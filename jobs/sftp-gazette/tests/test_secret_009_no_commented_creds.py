# criterion: @R-65.1
from pathlib import Path

def test_no_commented_sftp_password_in_source():
    text = Path(__file__).resolve().parents[1] / "services" / "sftp.py"
    content = text.read_text()
    assert "742mH273" not in content
    assert "TESTPUB" not in content
