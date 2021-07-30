import os


def build_example_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), "examples", filename)


PETSTORE_URL = "https://www.getpostman.com/collections/199d235c26b7e47325ba"
PETSTORE_PATH = build_example_path("petstore.postman_collection.json")

DECKOFCARDS_URL = "https://www.getpostman.com/collections/32538e3b6f596a43db77"
DECKOFCARDS_PATH = build_example_path("deckofcards.postman_collection.json")
