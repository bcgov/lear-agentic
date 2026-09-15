# Copyright © 2024 Province of British Columbia
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
"""Tests for the MRAS service.

Test suite to ensure that the MRAS service is working as expected.
"""
# criterion: @R-54.1 @R-54.2 @R-54.3

from http import HTTPStatus
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

from legal_api.services import MrasService

_MRAS_SERVICE_PATH = (
    Path(__file__).resolve().parents[3]
    / 'src'
    / 'legal_api'
    / 'services'
    / 'mras_service.py'
)


MRAS_CONTENT_TARGET = """
<Jurisdictions xmlns="http://mras.ca/schema/v1">
    <Jurisdiction>
        <JurisdictionID>SK</JurisdictionID>
        <NameEn>Saskatchewan</NameEn>
        <NameFr>Saskatchewan</NameFr>
        <RedirectUrl>asdf</RedirectUrl>
        <TargetProfileID>1111</TargetProfileID>
    </Jurisdiction>
    <Jurisdiction>
        <JurisdictionID>QC</JurisdictionID>
        <NameEn>Quebec</NameEn>
        <NameFr>Québec</NameFr>
        <RedirectUrl>asdf</RedirectUrl>
    </Jurisdiction>
    <Jurisdiction>
        <JurisdictionID>MB</JurisdictionID>
        <NameEn>Manitoba</NameEn>
        <NameFr>Manitoba</NameFr>
        <RedirectUrl>asdf</RedirectUrl>
    </Jurisdiction>
    <Jurisdiction>
        <JurisdictionID>AB</JurisdictionID>
        <NameEn>Alberta</NameEn>
        <NameFr>Alberta</NameFr>
        <RedirectUrl>asdfasdf</RedirectUrl>
        <TargetProfileID>2222</TargetProfileID>
    </Jurisdiction>
</Jurisdictions>
"""

MRAS_CONTENT_NO_TARGET = """
<Jurisdictions xmlns="http://mras.ca/schema/v1">
    <Jurisdiction>
        <JurisdictionID>SK</JurisdictionID>
        <NameEn>Saskatchewan</NameEn>
        <NameFr>Saskatchewan</NameFr>
        <RedirectUrl>asdf</RedirectUrl>
    </Jurisdiction>
    <Jurisdiction>
        <JurisdictionID>QC</JurisdictionID>
        <NameEn>Quebec</NameEn>
        <NameFr>Québec</NameFr>
        <RedirectUrl>asdf</RedirectUrl>
    </Jurisdiction>
    <Jurisdiction>
        <JurisdictionID>MB</JurisdictionID>
        <NameEn>Manitoba</NameEn>
        <NameFr>Manitoba</NameFr>
        <RedirectUrl>asdf</RedirectUrl>
    </Jurisdiction>
    <Jurisdiction>
        <JurisdictionID>AB</JurisdictionID>
        <NameEn>Alberta</NameEn>
        <NameFr>Alberta</NameFr>
        <RedirectUrl>asdf</RedirectUrl>
    </Jurisdiction>
</Jurisdictions>
"""

@pytest.mark.parametrize(
        'test_name, mock_status, mock_return, expected', [
            ('HAS_JURISDICTIONS', HTTPStatus.OK, MRAS_CONTENT_TARGET, [
                {
                    "id": "SK",
                    "name": "Saskatchewan",
                    "nameFr": "Saskatchewan",
                    "redirectUrl": "asdf",
                    "targetProfileId": "1111"
                },
                {
                    "id": "AB",
                    "name": "Alberta",
                    "nameFr": "Alberta",
                    "redirectUrl": "asdfasdf",
                    "targetProfileId": "2222"
                }
            ]),
            ('NO_JURISDICTIONS', HTTPStatus.OK, MRAS_CONTENT_NO_TARGET, []),
            ('ERROR', HTTPStatus.UNAUTHORIZED, None, None)
        ]
)
def test_get_jurisdictions(session, test_name, mock_status, mock_return, expected):
    """@R-54.1 — returns foreign jurisdictions for the given business with safe parser."""
    mock_response = MagicMock()
    mock_response.status_code = mock_status
    mock_response.content = mock_return
    with patch.object(requests, 'get', return_value=mock_response):
        jurisdictions = MrasService.get_jurisdictions('BC1234567')
        assert jurisdictions == expected


def test_mras_service_uses_safe_xml_parser():
    """@R-54.2 — fromstring is wired to XMLParser(resolve_entities=False, no_network=True)."""
    source = _MRAS_SERVICE_PATH.read_text(encoding='utf-8')
    assert 'XMLParser(' in source
    assert 'resolve_entities=False' in source
    assert 'no_network=True' in source
    assert 'fromstring(' in source
    assert 'parser=safe_parser' in source


def test_get_jurisdictions_rejects_external_entity_payload(session, tmp_path):
    """@R-54.3 — external entity content must not appear in jurisdiction results."""
    canary = tmp_path / 'mras-xxe-canary.txt'
    canary.write_text('SECRET_MRAS_XXE_CANARY', encoding='utf-8')
    # file:// URI; safe parser must not resolve/include this content.
    entity_uri = canary.as_uri()
    xxe_xml = f"""<?xml version="1.0"?>
<!DOCTYPE Jurisdictions [
  <!ENTITY xxe SYSTEM "{entity_uri}">
]>
<Jurisdictions xmlns="http://mras.ca/schema/v1">
    <Jurisdiction>
        <JurisdictionID>&xxe;</JurisdictionID>
        <NameEn>Saskatchewan</NameEn>
        <NameFr>Saskatchewan</NameFr>
        <RedirectUrl>asdf</RedirectUrl>
        <TargetProfileID>1111</TargetProfileID>
    </Jurisdiction>
</Jurisdictions>
"""
    mock_response = MagicMock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.content = xxe_xml.encode('utf-8')
    with patch.object(requests, 'get', return_value=mock_response):
        jurisdictions = MrasService.get_jurisdictions('BC1234567')

    assert 'SECRET_MRAS_XXE_CANARY' not in str(jurisdictions)
    # Fail closed or leave unresolved entity text empty — never expand the file.
    if jurisdictions:
        assert all(j.get('id') != 'SECRET_MRAS_XXE_CANARY' for j in jurisdictions)
        assert all(j.get('id') in (None, '', '&xxe;') for j in jurisdictions)
