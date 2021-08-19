import os


def build_example_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), "examples", filename)


OPENAPI_PETSTORE_YAML = build_example_path("petstore.openapi3.yaml")
OPENAPI_PETSTORE_JSON = build_example_path("petstore.openapi3.json")
SWAGGER_PETSTORE_YAML = build_example_path("petstore.swagger2.yaml")
SWAGGER_PETSTORE_JSON = build_example_path("petstore.swagger2.json")

SIMPLE_PETSTORE_OPENAPI_YAML = build_example_path("petstore.openapi_spec.yml")


POSTMAN_WORKSPACE_GLOBAL_VARIABLES_PATH = build_example_path("workspace.postman_globals.json")
POSTMAN_BIG_PETSTORE_PATH = build_example_path("big-petstore.postman_collection.json")
POSTMAN_BOOKSTORE_PATH = build_example_path("bookstore.postman_collection.json")
POSTMAN_BOOKSTORE_ENV_VARIABLES_PATH = build_example_path("bookstore.postman_environment.json")

POSTMAN_PETSTORE_URL = "https://www.getpostman.com/collections/199d235c26b7e47325ba"
POSTMAN_PETSTORE_PATH = build_example_path("petstore.postman_collection.json")

POSTMAN_DECKOFCARDS_URL = "https://www.getpostman.com/collections/32538e3b6f596a43db77"
POSTMAN_DECKOFCARDS_PATH = build_example_path("deckofcards.postman_collection.json")
