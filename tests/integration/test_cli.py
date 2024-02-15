import os
from pathlib import Path

import pytest

STATICS_PATH = "tests/integration/statics/"


@pytest.fixture
def readme() -> Path:
    filename = "TEST_README.md"
    readme = Path(filename)
    readme.write_text("<!-- begin env -->\n<!-- end env -->")

    yield readme

    readme.unlink()


def test_genvars(readme: Path):
    # Arrange
    static_file = Path(STATICS_PATH) / "expected.md"
    expected_content = static_file.read_text()

    # Act
    status_code = os.system(
        f"poetry run python3 -m genvars"
        f"tests.integration.statics.common.settings --output {readme.absolute()}"
    )

    # Assert
    assert status_code == 0

    real_text = readme.read_text()
    assert expected_content == real_text
