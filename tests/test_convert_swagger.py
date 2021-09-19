import pytest
from tests import utils
from pyclinic.swagger import Swagger
from pyclinic import swagger
from pyclinic.base import load_spec_file


FILE_TYPES = [
    utils.SWAGGER_PETSTORE_YAML,
    utils.SWAGGER_PETSTORE_JSON,
    utils.SWAGGER_SHORTCUT_JSON,
]

HOST = "https://api.app.shortcut.com"
BASE_PATH = "/api/v3"


@pytest.fixture(scope="session")
def pet_spec():
    return load_spec_file(utils.SWAGGER_PETSTORE_YAML)


@pytest.fixture(scope="session")
def shortcut_spec():
    return load_spec_file(utils.SWAGGER_SHORTCUT_JSON)


@pytest.mark.parametrize("file_type", FILE_TYPES)
def test_convert_swagger_file(file_type):
    spec = load_spec_file(file_type)
    assert spec


def test_petstore_find_requests(pet_spec):
    requests = swagger.find_requests(pet_spec)
    assert requests


def test_not_providing_host_or_base_path_raises_exception(shortcut_spec):
    """The Shorcut swagger spec file does not have a "host" or "basePath" field, so it must be provided at runtime.

    Not providing either will raise a ValueError.
    """
    with pytest.raises(ValueError):
        swagger.find_requests(shortcut_spec)


def test_shortcut_find_requests(shortcut_spec):
    folders = swagger.find_requests(shortcut_spec, host=HOST, base_path=BASE_PATH)
    assert folders
    assert folders["Epics"]["get_epic_comment"]


def test_swagger_runner_shortcut():
    runner = Swagger(utils.SWAGGER_SHORTCUT_JSON, host=HOST, base_path=BASE_PATH)
    assert runner
    runner.show_variables()
    runner.show_folders()
    runner.Stories.help()
    runner.Stories.create_story.help()


def test_swagger_runner_petstore():
    runner = Swagger(utils.SWAGGER_PETSTORE_YAML)
    assert runner
    runner.show_variables()
    runner.show_folders()
    runner.Pet.help()
    runner.Pet.add_pet.help()


def test_swagger_global_request():
    headers = {"headers": {"Authorization": "Bearer 123"}}
    runner = Swagger(utils.SWAGGER_PETSTORE_JSON, global_request=headers, variables={"petId": 123})
    runner.Pet.help()
    get_pet = runner.Pet.get_pet_by_id
    assert get_pet.request["method"] == "GET"
    assert get_pet.request["url"] == "https://petstore.swagger.io/v2/pet/123"
    assert get_pet.request["headers"] == headers["headers"]
