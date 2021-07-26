import os
import pytest
import pyclinic.model_parser as parser


@pytest.fixture
def model():
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


def test_parse_json_to_model(model):
    assert model is not None
    assert "user_id: str" in model


@pytest.fixture
def write_model_to_file(model):
    file_path = parser.write_model_to_file(model, "test_model.py")
    yield file_path
    os.remove(file_path)


def test_model_file_is_created(write_model_to_file):
    file_path = write_model_to_file
    assert os.path.exists(file_path)
