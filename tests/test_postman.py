from pyclinic import postman
from tests import utils


def test_load_petstore_from_url():
    collection = postman.load_postman_collection_from_url(utils.PETSTORE_URL)
    assert collection.info.name == "Swagger Petstore"
    assert len(collection.folders) == 1


def test_load_deckofcards_from_url():
    collection = postman.load_postman_collection_from_url(utils.DECKOFCARDS_URL)
    assert collection.info.name == "Deck of Cards"
    assert collection.folders is None


def test_load_petstore_from_file():
    collection = postman.load_postman_collection_from_file(utils.PETSTORE_PATH)
    assert collection.info.name == "Swagger Petstore"
    assert len(collection.folders) == 1


def test_load_deckofcards_from_file():
    collection = postman.load_postman_collection_from_file(utils.DECKOFCARDS_PATH)
    assert collection.info.name == "Deck of Cards"
    assert collection.folders is None


def test_petstore_to_pydantic():
    collection = postman.load_postman_collection_from_file(utils.PETSTORE_PATH)
    assert collection.info.name == "Swagger Petstore"
    assert collection.folders[0].name == "pets"
    assert collection.folders[0].item[0].name == "List all pets"


def test_deckofcards_to_pydantic():
    collection = postman.load_postman_collection_from_file(utils.DECKOFCARDS_PATH)
    assert collection.info.name == "Deck of Cards"
    assert collection.item[0].name == "Create shuffled deck"


def test_find_petstore_response_bodies():
    """Petstore uses folders, so bodies has an extra layer - hence navigating into 'pets'."""
    collection = postman.load_postman_collection_from_file(utils.PETSTORE_PATH)
    bodies = postman.find_response_bodies(collection)
    assert bodies["pets"]["Create a pet"] is not None


def test_find_deckofcards_response_bodies():
    """Deck of cards has zero folders."""
    collection = postman.load_postman_collection_from_file(utils.DECKOFCARDS_PATH)
    bodies = postman.find_response_bodies(collection)
    assert bodies["Create shuffled deck"] is not None
