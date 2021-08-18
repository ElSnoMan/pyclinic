from typing import Dict
import pytest

from tests.bookstore import account_service

from faker import Faker


@pytest.fixture
def credentials() -> Dict:
    fake = Faker()
    return {"userName": fake.name(), "password": "Pa$$w0rd"}


def test_create_user(credentials):
    user = account_service.create_user(credentials)
    assert user.username == credentials.get("userName")


def test_authorize_user(credentials):
    _, token = account_service.create_authorized_user(credentials)
    assert token.status == "Success", "Generate Token failed"
    assert account_service.is_authorized(credentials)


def test_get_user(credentials):
    user, token = account_service.create_authorized_user(credentials)
    found_user = account_service.get_user(user.user_id, token.token)
    assert found_user.username == user.username


def test_delete_user(credentials):
    user, token = account_service.create_authorized_user(credentials)
    response = account_service.delete_user(user.user_id, token.token)
    assert response.status_code == 204
