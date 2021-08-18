from typing import Dict, Tuple
from requests import Response
from pyclinic.postman import Postman
from tests import utils
from tests.bookstore.models.account_model import Nate, Token, User


runner = Postman(utils.BOOKSTORE_PATH, utils.BOOKSTORE_ENV_VARIABLES_PATH)
runner.show_folders()
runner.show_variables()


def create_user(credentials: Dict) -> User:
    response = runner.Account.create_user(data=credentials)
    return User(**response.json())


def authorize_user(credentials: Dict) -> Token:
    response = runner.Account.generate_token(data=credentials)
    return Token(**response.json())


def create_authorized_user(credentials: Dict) -> Tuple[User, Token]:
    user = create_user(credentials)
    token = authorize_user(credentials)
    return user, token


def is_authorized(credentials: Dict) -> bool:
    response = runner.Account.is_authorized(data=credentials)
    return response.json()


def get_user(user_id: str, token: str) -> Nate:
    variables = {
        "USER_ID": user_id,
        "TOKEN": token,
    }
    response = runner.Account.get_user(variables)
    return Nate(**response.json())


def delete_user(user_id: str, token: str) -> Response:
    variables = {
        "USER_ID": user_id,
        "TOKEN": token,
    }
    return runner.Account.delete_user(variables)
