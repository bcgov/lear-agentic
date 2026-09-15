# criterion: @R-04.1
# Copyright © 2026 Province of British Columbia
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
"""Parameterized IN-clause helpers for VULN-002 (pure functions; no Oracle)."""
import importlib.util
from pathlib import Path

import pytest

_UTILS_PATH = (
    Path(__file__).resolve().parents[1] / 'src' / 'colin_api' / 'utils' / '__init__.py'
)


def _load_utils():
    """Load utils module from source without importing the full colin_api package."""
    spec = importlib.util.spec_from_file_location('colin_api_utils_vuln002', _UTILS_PATH)
    module = importlib.util.module_from_spec(spec)
    # utils imports flask.current_app at module level for other helpers
    import sys
    from unittest.mock import MagicMock
    sys.modules.setdefault('flask', MagicMock())
    spec.loader.exec_module(module)
    return module


_utils = _load_utils()
build_in_clause = _utils.build_in_clause
build_cooper_reset_filings_query = _utils.build_cooper_reset_filings_query


def test_build_in_clause_uses_placeholders_not_literals():
    """@R-04.1 — SQL fragment is placeholders; values live only in binds."""
    injection = "x' OR '1'='1"
    clause, binds = build_in_clause([injection, 'CP1234567'], 'ident')

    assert clause == ':ident_0,:ident_1'
    assert binds == {'ident_0': injection, 'ident_1': 'CP1234567'}
    assert injection not in clause
    assert "'" not in clause


def test_build_in_clause_rejects_empty_list():
    """@R-04.1 — empty lists must not produce a broken IN () fragment."""
    with pytest.raises(ValueError):
        build_in_clause([], 'ident')


def test_build_in_clause_rejects_bad_prefix():
    """@R-04.1 — bind name stem must be safe alphanumeric."""
    with pytest.raises(ValueError):
        build_in_clause(['CP1'], 'id;drop')


def test_reset_query_binds_identifiers():
    """@R-04.2 — identifiers appear in binds, not as quoted SQL literals."""
    payload = "CP1' OR '1'='1"
    sql, binds = build_cooper_reset_filings_query(
        '2019-08-10', '9999-12-31', identifiers=[payload]
    )
    assert f"'{payload}'" not in sql
    assert ':ident_0' in sql
    assert binds['ident_0'] == payload
    assert binds['start_date'] == '2019-08-10'
    assert binds['end_date'] == '9999-12-31'


def test_reset_query_binds_filing_types():
    """@R-04.3 — filing_types appear in binds, not as quoted SQL literals."""
    payload = "OTANN'; DROP TABLE event--"
    sql, binds = build_cooper_reset_filings_query(
        '2019-08-10', '9999-12-31', filing_types=[payload, 'BEINC']
    )
    assert f"'{payload}'" not in sql
    assert ':ftype_0' in sql and ':ftype_1' in sql
    assert binds['ftype_0'] == payload
    assert binds['ftype_1'] == 'BEINC'
