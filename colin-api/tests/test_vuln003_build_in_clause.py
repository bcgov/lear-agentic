# criterion: @R-53.1
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
"""Parameterized IN-clause helpers for VULN-003 string-typed paths (no Oracle)."""
import importlib.util
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

_UTILS_PATH = (
    Path(__file__).resolve().parents[1] / 'src' / 'colin_api' / 'utils' / '__init__.py'
)


def _load_utils():
    """Load utils module from source without importing the full colin_api package."""
    spec = importlib.util.spec_from_file_location('colin_api_utils_vuln003', _UTILS_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault('flask', MagicMock())
    spec.loader.exec_module(module)
    return module


_utils = _load_utils()
build_in_clause = _utils.build_in_clause
build_cooper_reset_filings_query = _utils.build_cooper_reset_filings_query


def test_build_in_clause_binds_string_injection_payload():
    """@R-53.1 — string values appear only in the bind map."""
    injection = "CP1' OR '1'='1"
    clause, binds = build_in_clause([injection, 'CP1234567'], 'corp')

    assert clause == ':corp_0,:corp_1'
    assert binds == {'corp_0': injection, 'corp_1': 'CP1234567'}
    assert injection not in clause
    assert "'" not in clause


def test_build_in_clause_rejects_empty_and_bad_prefix():
    """@R-53.1 — empty lists / unsafe prefixes fail closed."""
    with pytest.raises(ValueError):
        build_in_clause([], 'corp')
    with pytest.raises(ValueError):
        build_in_clause(['CP1'], 'id;drop')


def test_reset_query_binds_identifiers_and_filing_types():
    """@R-53.2 — cooper reset string filters use binds (extends VULN-002)."""
    ident = "CP1' OR '1'='1"
    ftype = "OTANN'; DROP TABLE event--"
    sql, binds = build_cooper_reset_filings_query(
        '2019-08-10', '9999-12-31', identifiers=[ident], filing_types=[ftype]
    )
    assert f"'{ident}'" not in sql
    assert f"'{ftype}'" not in sql
    assert ':ident_0' in sql and ':ftype_0' in sql
    assert binds['ident_0'] == ident
    assert binds['ftype_0'] == ftype


def test_string_typed_call_sites_no_longer_interpolate_stringify_list():
    """@R-53.3 — string-typed model paths no longer call stringify_list inline."""
    models = Path(__file__).resolve().parents[1] / 'src' / 'colin_api' / 'models'
    # Files / patterns that must not stringify string-typed IN lists
    checks = {
        'reset.py': [
            'stringify_list(self.identifiers)',
            'stringify_list(self.filing_types)',
            'stringify_list(corp_nums)',
        ],
        'business.py': [
            'stringify_list(identifiers)',
            'stringify_list(corp_types)',
        ],
        'filing_type.py': [
            'stringify_list(matching_filing_types)',
        ],
    }
    for filename, forbidden in checks.items():
        source = (models / filename).read_text(encoding='utf-8')
        for needle in forbidden:
            assert needle not in source, f'{filename} still interpolates {needle}'
