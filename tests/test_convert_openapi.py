import pytest
from tests import utils
from pyclinic.openapi import OpenApi


FILE_TYPES = [
    utils.OPENAPI_PETSTORE_JSON,
    utils.OPENAPI_PETSTORE_YAML,
]


@pytest.mark.parametrize("file_type", FILE_TYPES)
def test_convert_openapi_spec(file_type):
    runner = OpenApi(file_type)
    runner.show_variables()
    runner.show_folders()


def test_convert_openapi_spec_with_file_not_found():
    with pytest.raises(FileNotFoundError):
        OpenApi("invalid_file.json")


def test_convert_openapi_spec_with_invalid_file_extension():
    with pytest.raises(ValueError):
        OpenApi(utils.build_example_path("invalid_extension.txt"))


@pytest.fixture(scope="module")
def runner():
    _runner = OpenApi(utils.OPENAPI_PETSTORE_JSON)
    _runner.show_variables()
    _runner.show_folders()
    return _runner


def test_create_a_pet(runner: OpenApi):
    payload = {
        "id": 0,
        "category": {"id": 0, "name": "string"},
        "name": "doggie",
        "photoUrls": ["string"],
        "tags": [{"id": 0, "name": "string"}],
        "status": "available",
    }
    add_pet_response = runner.Pet.add_pet(json=payload)
    pet_id = add_pet_response.json()["id"]
    assert isinstance(pet_id, int)


def test_find_pets_by_status(runner: OpenApi):
    params = {"status": ["available", "pending", "sold"]}
    response = runner.Pet.find_pets_by_status(params=params)
    assert response.ok
