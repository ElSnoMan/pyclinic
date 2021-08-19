from typing import Dict
from tests import utils
import pytest
from pyclinic import openapi
from pyclinic.openapi import OpenApi


@pytest.fixture
def spec() -> Dict:
    return openapi.load_openapi_spec_from_file(utils.SIMPLE_PETSTORE_OPENAPI_YAML)


def test_read_yaml(spec: Dict):
    assert spec["info"]["title"] == "Swagger Petstore"


def test_extract_base_url_from_spec(spec: Dict):
    url, variables = openapi.extract_base_url_from_spec(spec)
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
