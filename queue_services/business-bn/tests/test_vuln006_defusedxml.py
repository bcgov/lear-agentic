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
"""Safe CRA BN Hub XML parsing (VULN-006 / defusedxml).

# criterion: @R-64.1 @R-64.2 @R-64.3
"""
from pathlib import Path

import defusedxml.ElementTree as Et
import pytest
from defusedxml.common import EntitiesForbidden

_PROCESSORS = Path(__file__).resolve().parents[1] / "src" / "business_bn" / "bn_processors"
_PROCESSOR_FILES = (
    "registration.py",
    "admin.py",
    "change_of_registration.py",
    "dissolution_or_put_back_on.py",
)


def test_bn_processors_import_defusedxml_elementtree():
    """@R-64.1 — CRA BN Hub processors parse XML via defusedxml.ElementTree."""
    for name in _PROCESSOR_FILES:
        source = (_PROCESSORS / name).read_text(encoding="utf-8")
        assert "import defusedxml.ElementTree as Et" in source, name
        assert "import xml.etree.ElementTree as Et" not in source, name
        assert "Et.fromstring(" in source, name


def test_defusedxml_parses_benign_acknowledgement():
    """@R-64.2 — benign CRA acknowledgement XML still parses."""
    xml = "<SBNAcknowledgement><status>OK</status></SBNAcknowledgement>"
    root = Et.fromstring(xml)
    assert root.tag == "SBNAcknowledgement"
    assert root.find("status").text == "OK"


def test_defusedxml_rejects_entity_expansion(tmp_path):
    """@R-64.3 — entity expansion / external entities are forbidden."""
    canary = tmp_path / "bn-xxe-canary.txt"
    canary.write_text("SECRET_BN_XXE_CANARY", encoding="utf-8")
    xxe_xml = f"""<?xml version="1.0"?>
<!DOCTYPE SBNAcknowledgement [
  <!ENTITY xxe SYSTEM "{canary.as_uri()}">
]>
<SBNAcknowledgement>&xxe;</SBNAcknowledgement>
"""
    with pytest.raises((EntitiesForbidden, Et.ParseError, ValueError)):
        Et.fromstring(xxe_xml)
