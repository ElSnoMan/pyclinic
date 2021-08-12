from typing import Dict, List
import pytest
import requests
from pydantic import BaseModel, Field
from faker import Faker

BASE_URL = "https://demoqa.com"


class User(BaseModel):
    user_id: str = Field(..., alias="userID")
    username: str
    books: List[Dict]


@pytest.fixture
def credentials() -> Dict:
    fake = Faker()
    return {"userName": fake.name(), "password": "Pa$$w0rd"}


@pytest.fixture
def user(credentials) -> User:
    response = requests.post(BASE_URL + "/Account/v1/User", json=credentials)
    return User(**response.json())


def test_create_user(user, credentials):
    assert user.username == credentials.get("userName")


def test_authorize_user(user: User):
    pass
