import os

import pyclinic.model_parser as parser
import pytest
from pyclinic import postman
from pyclinic.models.postman_collection_model import PostmanCollection

from tests import utils


@pytest.fixture
def bookstore_user_model():
    return parser.json_to_model(
        JSON={
            "userId": "string",
            "username": "string",
            "books": [
                {
                    "isbn": "string",
                    "title": "string",
                    "subTitle": "string",
                    "author": "string",
                    "publish_date": "2021-07-26T19:59:40.552Z",
                    "publisher": "string",
                    "pages": 0,
                    "description": "string",
                    "website": "string",
                }
            ],
        }
    )


@pytest.fixture
def write_model_to_file(bookstore_user_model):
    file_path = parser.write_model_to_file(bookstore_user_model, "test_model.py")
    yield file_path
    os.remove(file_path)


@pytest.fixture
def petstore_model() -> PostmanCollection:
    file_path = utils.build_example_path("petstore.postman_collection.json")
    collection = postman.load_postman_collection_from_file(file_path)
    return collection


def test_parse_json_to_model(bookstore_user_model):
    assert bookstore_user_model is not None
    assert "user_id: str" in bookstore_user_model


def test_model_file_is_created(write_model_to_file):
    file_path = write_model_to_file
    assert os.path.exists(file_path)
