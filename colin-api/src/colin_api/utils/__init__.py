# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Time conversion methods."""
import datetime

from flask import current_app
from pytz import timezone


def convert_to_json_date(thedate: datetime.datetime) -> str:
    """Convert datetime to string formatted as YYYY-MM-DD, per JSON Schema specs."""
    if not thedate:
        return None
    try:
        return thedate.strftime('%Y-%m-%d')
    except Exception as err:  # pylint: disable=broad-except; want to return None in all cases where convert failed
        current_app.logger.debug(f'Tried to convert {thedate}, but failed: {err}')
        return None


def convert_to_json_datetime(thedate: datetime.datetime) -> str:
    """Convert datetime to string formatted as YYYY-MM-SSTHH:MM:SS+00:00, per JSON Schema specs."""
    if not thedate:
        return None
    try:
        # timezone info not in var (they are pacific times so add timezone)
        thedate = datetime.datetime(thedate.year,
                                    thedate.month,
                                    thedate.day,
                                    thedate.hour,
                                    thedate.minute,
                                    thedate.second)
        # treat date as naive date and add timezone by using localize function
        thedate = timezone('US/Pacific').localize(thedate)
        # convert to utc time
        thedate = thedate.astimezone(timezone('UTC'))
        # return as string
        return thedate.strftime('%Y-%m-%dT%H:%M:%S-00:00')
    except Exception as err:  # pylint: disable=broad-except; want to return None in all cases where convert failed
        current_app.logger.debug(f'Tried to convert {thedate}, but failed: {err}')
        return None


def convert_to_pacific_time(thedate: str) -> str:
    """Convert the datetime string to pacific time string."""
    try:
        # tries converting two formats before bailing
        try:
            datetime_obj = datetime.datetime.strptime(thedate, '%Y-%m-%dT%H:%M:%S.%f+00:00')
        except Exception:  # pylint: disable=broad-except;
            datetime_obj = datetime.datetime.strptime(thedate, '%Y-%m-%dT%H:%M:%S+00:00')
        datetime_utc = datetime_obj.replace(tzinfo=timezone('UTC'))
        datetime_pst = datetime_utc.astimezone(timezone('US/Pacific'))
        return datetime_pst.strftime('%Y-%m-%dT%H:%M:%S')
    except Exception as err:  # pylint: disable=broad-except; want to return None in all cases where convert failed
        current_app.logger.error(f'Tried to convert {thedate}, but failed: {err}')
        raise err


def build_in_clause(values: list, prefix: str):
    """Build a parameterized SQL IN-list fragment and bind map for cx_Oracle.

    Use this for untrusted / string-typed values. Do not interpolate those
    values into SQL with stringify_list.

    Returns:
        (sql_fragment, binds) where sql_fragment is like ':pref_0,:pref_1'
        and binds maps those names to the original values.
    """
    if not values:
        raise ValueError('values must be a non-empty list for an IN clause')
    if not prefix or not str(prefix).replace('_', '').isalnum():
        raise ValueError('prefix must be a non-empty alphanumeric bind name stem')

    binds = {}
    placeholders = []
    for index, value in enumerate(values):
        key = f'{prefix}_{index}'
        placeholders.append(f':{key}')
        binds[key] = value
    return ','.join(placeholders), binds


def build_cooper_reset_filings_query(start_date: str, end_date: str,
                                     identifiers: list = None,
                                     filing_types: list = None):
    """Build the cooper reset lookup SQL and bind map (VULN-002 / VULN-003).

    Request-sourced identifiers / filing_types are bound, never stringified.
    """
    query_string = """
            select event.event_id, event.corp_num, filing_typ_cd
            from event
            join filing on filing.event_id = event.event_id
            left join filing_user on event.event_id = filing_user.event_id
            where filing_user.user_id in ('COOPER', 'BCOMPS')
            AND event.event_timestmp>=TO_DATE(:start_date, 'yyyy-mm-dd')
            AND event.event_timestmp<=TO_DATE(:end_date, 'yyyy-mm-dd')
        """
    binds = {
        'start_date': start_date,
        'end_date': end_date,
    }

    if identifiers:
        clause, ident_binds = build_in_clause(identifiers, 'ident')
        query_string += f' AND event.corp_num in ({clause})'
        binds.update(ident_binds)

    if filing_types:
        clause, type_binds = build_in_clause(filing_types, 'ftype')
        query_string += f' AND filing.filing_typ_cd in ({clause})'
        binds.update(type_binds)

    query_string += '  ORDER BY event.event_timestmp desc'
    return query_string, binds


def stringify_list(list_orig: list) -> str:
    """Stringify a trusted numeric ID list for SQL IN clauses (legacy helper).

    Not safe for request-sourced or string-typed values — use build_in_clause /
    bind variables instead (VULN-002 / VULN-003). Residual: internal integer
    event_id / addr_id lists may still call this helper.
    """
    list_str = ''
    for item in list_orig:
        # remove any spaces or end brackets to avoid sql injection that could end the list and execute another command
        list_str += ("'" + str(item) + "',").replace(' ', '').replace(')', '')
    if list_str:
        list_str = list_str[:-1]
    return list_str


def delete_from_table_by_event_ids(cursor, event_ids: list, table: str, column: str = 'start_event_id'):
    """Delete rows with given event ids from given table.

    Residual (VULN-003): event_ids are treated as trusted integer IDs from
    prior COLIN queries; still uses stringify_list rather than binds.
    """
    try:
        # table is a value set by the code: not possible to be sql injected from a request
        cursor.execute(f"""
            DELETE FROM {table}
            WHERE {column} in ({stringify_list(event_ids)})
        """)
    except Exception as err:
        current_app.logger.error(f'Error in Reset: Failed to delete rows for events {event_ids} in table: {table}')
        raise err


def get_max_value(cursor, corp_num: str, table: str, column: str):
    """Get the max value for a column in a table for a business."""
    try:
        cursor.execute(
            f"""
            select max({column}) from {table} where corp_num=:corp_num
            """,
            corp_num=corp_num
        )
        return cursor.fetchone()[0]

    except Exception as err:
        current_app.logger.error(f'Error getting max {column}.')
        raise err


def convert_to_snake(inputstring: str):
    """Convert inputstring from camel case to snake case."""
    return ''.join('_' + char.lower() if char.isupper() else char for char in inputstring).lstrip('_')
