""" Version 3 of OpenAPI

More info:
    https://swagger.io/docs/specification/basic-structure/
"""

from typing import Dict, Optional, Tuple

from pyclinic.base import METHODS, BaseRunner, map_requests_to_executable_functions
from pyclinic.normalize import normalize_class_name, normalize_function_name


def build_url(spec: Dict, server: str = None) -> Tuple[str, Dict]:
    """Build the BASE_URL to be used by all requests in the spec.

    Args:
        spec: The loaded OpenAPI 3 spec.
        server: The BASE_URL to use for all requests.

    Returns:
        A tuple of the first BASE_URL (as default) and a variables dictionary that sets the BASE_URL.

    Exceptions:
        ValueError: If the "servers" section is not found or is empty.
    """
    base_url = server or spec["servers"][0]["url"]
    variables = {"BASE_URL": base_url}
    return base_url, variables


def find_requests(spec: Dict, server: str = None) -> Dict:
    """Find all the requests in the spec and format them into our flat "folders" dictionary.

    Args:
        spec: The loaded OpenAPI 3 spec.
        server: The BASE_URL to use for the requests.

    Returns:
        A dictionary like:
        {
            'pets': {
                'create_a_pet': {'method': 'POST', 'url': 'http://petstore.swagger.io/v1/pets'},
                'info_for_a_pet': {'method': 'GET', 'url': 'http://petstore.swagger.io/v1/pets/:petId'},
                'list_pets': {'method': 'GET', 'url': 'http://petstore.swagger.io/v1/pets?limit=-71686804'},
            },
        }
    """
    url, _ = build_url(spec, server)
    paths = spec["paths"]
    folders = {}

    for path in paths.keys():
        folder_name = path.split("/")[1]  # /pets/{petId} => pets
        folder_name = normalize_class_name(folder_name)
        if folder_name not in folders:
            folders[folder_name] = {}
        for method in [k for k in paths[path].keys() if k in METHODS]:
            function_name = normalize_function_name(paths[path][method]["operationId"])
            folders[folder_name][function_name] = {"method": method.upper(), "url": url + path}

    return folders


class OpenApi(BaseRunner):
    """Instance of a OpenAPI Spec Runner with executable request functions.

    Args:
        spec_path: The path to the OpenApi spec file (.yaml | .yml | .json)
        variables: An optional dict of variables to be used by OpenApi

    Format:
        OpenApi.ExecutableFolder.ExecutableRequest(**kwargs)

    Examples:
        # Instantiate OpenApi with any variables
        runner = OpenApi(spec_path, user_variables={"USERNAME": "foo", "PASSWORD": "bar"})

        # Then call the request function
        runner.Pets.list_all_pets()
        runner.Accounts.create_a_user(data={"username": "johndoe", "password": "secret"})

    * You can override the Request that the endpoint function sends. Here are some common options:
        headers: A list of headers to send with the request.
        method: The HTTP method to use.
        url: The URL to send the request to.
        params: A dictionary of parameters to send with the request.
        data: The body of the request.
    """

    def __init__(
        self,
        spec_path: str,
        global_request: Optional[Dict] = None,
        variables: Optional[Dict] = None,
    ):
        super().__init__(spec_path, global_request, variables)
        self.folders = self.__load()

    def __load(self):
        reqs = find_requests(self.spec)
        return map_requests_to_executable_functions(reqs, self.global_request, self.variables)
