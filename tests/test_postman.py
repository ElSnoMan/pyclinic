import pytest
import requests
from jsonpath_ng import parse
from pyclinic import postman
from pyclinic.models.postman_collection_model import PostmanRequest

from pyclinic.models.postman_collection_model import PostmanCollection
from pyclinic.postman import Postman
from tests import utils


@pytest.fixture
def load_collection() -> PostmanCollection:
    def _load(example_filepath: str):
        return postman.load_postman_collection_from_file(example_filepath)

    return _load


def test_load_big_petstore_from_file():
    collection = postman.load_postman_collection_from_file(utils.BIG_PETSTORE_PATH)
    assert collection.info.name == "Big Petstore"


def test_load_petstore_from_url():
    collection = postman.load_postman_collection_from_url(utils.PETSTORE_URL)
    assert collection.info.name == "Swagger Petstore"
    assert collection.item[-1].get("name") == "Is 10 Even?"


def test_load_deckofcards_from_url():
    collection = postman.load_postman_collection_from_url(utils.DECKOFCARDS_URL)
    assert collection.info.name == "Deck of Cards"


def test_load_petstore_from_file():
    collection = postman.load_postman_collection_from_file(utils.PETSTORE_PATH)
    assert collection.info.name == "Swagger Petstore"


def test_load_deckofcards_from_file():
    collection = postman.load_postman_collection_from_file(utils.DECKOFCARDS_PATH)
    assert collection.info.name == "Deck of Cards"


def test_petstore_to_pydantic():
    collection = postman.load_postman_collection_from_file(utils.PETSTORE_PATH)
    assert collection.info.name == "Swagger Petstore"
    assert collection.item[0].get("name") == "pets"
    assert collection.item[0]["item"][0].get("name") == "List all pets"


def test_deckofcards_to_pydantic():
    collection = postman.load_postman_collection_from_file(utils.DECKOFCARDS_PATH)
    assert collection.info.name == "Deck of Cards"
    assert collection.item[0].get("name") == "Folder 1"


def test_find_petstore_response_bodies():
    collection = postman.load_postman_collection_from_file(utils.PETSTORE_PATH)
    folders = postman.map_response_bodies_to_folders(collection)
    assert folders["pets"]["Create a pet"] is not None
    assert folders["Root"]["Is 10 Even?"] is not None


def test_find_deckofcards_response_bodies():
    collection = postman.load_postman_collection_from_file(utils.DECKOFCARDS_PATH)
    folders = postman.map_response_bodies_to_folders(collection)
    expected = ["Root", "Folder 1", "Folder 1.1", "Folder 2"]
    assert list(folders.keys()) == expected


def test_convert_single_PostmanRequest_with_variables_to_request(load_collection):
    COLLECTION = load_collection(utils.PETSTORE_PATH)

    req = PostmanRequest(**COLLECTION.item[0]["item"][0].get("request"))
    REQUEST = postman.build_request_to_send(COLLECTION, req)

    response = requests.request(**REQUEST)
    assert response.status_code == 404


def test_find_request_ascendants(load_collection):
    COLLECTION = load_collection(utils.DECKOFCARDS_PATH)

    matches = [match for match in parse("$..[*] where response").find(COLLECTION.item)]
    item = matches[2]
    ascendants = postman.find_request_ascendants(item)

    assert ascendants == ["Root", "Folder 1", "Folder 1.1"]


def test_postman_runner_e2e():
    path = utils.build_example_path(utils.PETSTORE_PATH)
    runner = Postman(path)

    assert runner.Pets.list_all_pets().status_code == 404
    response = runner.Root.is_10_even()
    assert response.ok
    assert response.json()["iseven"] is True


def test_postman_runner_e2e_with_big_petstore():
    path = utils.build_example_path(utils.BIG_PETSTORE_PATH)
    runner = Postman(path)
    response = runner.PetId.find_pet_by_id()
    assert response.status_code == 404
