from scripts import pyproject


def test_get_pyproject_version():
    version = pyproject.get_version()
    assert version == "0.3.2"
