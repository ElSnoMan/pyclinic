from typing import Dict, Tuple
from requests import Response
from pyclinic.postman import Postman
from tests import utils


runner = Postman(utils.BOOKSTORE_PATH, utils.BOOKSTORE_ENV_VARIABLES_PATH)
runner.show_folders()
runner.show_variables()


def create_user(credentials: Dict) -> Dict:
    response = runner.Account.create_user(data=credentials)
    return response.json()


def authorize_user(credentials: Dict) -> Dict:
    response = runner.Account.generate_token(data=credentials)
    return response.json()


def create_authorized_user(credentials: Dict) -> Tuple[Dict, Dict]:
    user = create_user(credentials)
    token = authorize_user(credentials)
    return user, token


def is_authorized(credentials: Dict) -> bool:
    response = runner.Account.is_authorized(data=credentials)
    return response.json()


def get_user(user_id: str, token: str) -> Dict:
    variables = {
        "USER_ID": user_id,
        "TOKEN": token,
    }
    response = runner.Account.get_user(variables)
    return response.json()


def delete_user(user_id: str, token: str) -> Response:
    variables = {
        "USER_ID": user_id,
        "TOKEN": token,
    }
    return runner.Account.delete_user(variables)
