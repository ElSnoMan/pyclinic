import os

import pyclinic.model_parser as parser
import pytest


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


def test_parse_json_to_model(bookstore_user_model):
    assert bookstore_user_model is not None
    assert "user_id: str" in bookstore_user_model


def test_model_file_is_created(write_model_to_file):
    file_path = write_model_to_file
    assert os.path.exists(file_path)


def test_json_to_model_receives_none_or_empty():
    result = parser.json_to_model(None)
    assert result == ""
    result = parser.json_to_model("")
    assert result == ""
