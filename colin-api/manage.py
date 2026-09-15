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

"""Manage the database and some other items required to run the API
"""
import logging

import click

from colin_api import create_app

APP = create_app()


@click.group()
def cli():
    """COLIN API management commands (replaces Flask-Script Manager)."""


@cli.command('list_routes')
def list_routes():
    """Print registered URL rules."""
    output = []
    # Flask 2.3+ requires SERVER_NAME for url_for outside a request; list paths from the map.
    for rule in APP.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods or []))
        line = ('{:50s} {:20s} {}'.format(rule.endpoint, methods, rule.rule))
        output.append(line)

    for line in sorted(output):
        print(line)


if __name__ == '__main__':
    logging.log(logging.INFO, 'Running the Manager')
    cli()
