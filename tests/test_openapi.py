from typing import Dict
from tests import utils
import pytest
from pyclinic import openapi
from pyclinic.openapi import OpenApi
from pyclinic.base import load_spec_file


@pytest.fixture
def spec() -> Dict:
    return load_spec_file(utils.SIMPLE_PETSTORE_OPENAPI_YAML)


def test_read_yaml(spec: Dict):
    assert spec["info"]["title"] == "Swagger Petstore"


def test_extract_base_url_from_spec(spec: Dict):
    url, variables = openapi.build_url(spec)
    assert url == "http://petstore.swagger.io/v1"
    assert variables == {"BASE_URL": url}


def test_find_requests(spec: Dict):
    expected = {
        "Pets": {
            "list_pets": {"method": "GET", "url": "http://petstore.swagger.io/v1/pets"},
            "create_pets": {"method": "POST", "url": "http://petstore.swagger.io/v1/pets"},
            "show_pet_by_id": {"method": "GET", "url": "http://petstore.swagger.io/v1/pets/{petId}"},
        }
    }
    folders = openapi.find_requests(spec)
    assert folders == expected


def test_openapi_runner():
    runner = OpenApi(utils.SIMPLE_PETSTORE_OPENAPI_YAML)
    response = runner.Pets.show_pet_by_id(variables={"petId": 123})

    assert response.status_code == 404


def test_openapi_global_request():
    headers = {"headers": {"Authorization": "Bearer 123"}}
    runner = OpenApi(utils.SIMPLE_PETSTORE_OPENAPI_YAML, global_request=headers, variables={"petId": 123})
    show_pet = runner.Pets.show_pet_by_id
    assert show_pet.request["method"] == "GET"
    assert show_pet.request["url"] == "http://petstore.swagger.io/v1/pets/123"
    assert show_pet.request["headers"] == headers["headers"]
