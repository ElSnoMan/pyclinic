""" Version 2 of OpenAPI (fka Swagger or Swagger 2)

More info:
    https://swagger.io/docs/specification/2-0/basic-structure/
"""

from typing import Dict, Optional

from pyclinic import base
from pyclinic.base import METHODS, BaseRunner, logger
from pyclinic.normalize import normalize_class_name, normalize_function_name


def build_url(host: str, base_path: str, path: str) -> str:
    """Build a URL based on the values from the Swagger2 spec file.

    Returns:
        A URL like:
        https://api.app.shortcut.com/api/v3/search

    Examples:
        host:           "https://api.app.shortcut.com"
        base_path:      "/api/v3"
        path:           "/search"
    """
    logger.debug(f"Attempting to build URL with host={host}, base_path={base_path}, path={path}")

    # 1. Normalize host
    if not host.startswith("https"):
        host = "https://" + host

    # 2 Normalize base_path
    if base_path.endswith("/"):
        base_path = base_path[:-1]

    # 3. Prefix base to path
    path = path.replace(base_path, "")
    return host + base_path + path


def find_requests(spec: Dict, host: str = None, base_path: str = None) -> Dict:
    """
    Returns a Dict like:
    {
        'pets': {
            'create_a_pet': {'method': 'POST', 'url': 'http://petstore.swagger.io/v1/pets'},
            'info_for_a_pet': {'method': 'GET', 'url': 'http://petstore.swagger.io/v1/pets/:petId'},
            'list_pets': {'method': 'GET', 'url': 'http://petstore.swagger.io/v1/pets?limit=-71686804'},
        },
    }
    """
    paths = spec["paths"]
    host = host or spec.get("host")
    base_path = base_path or spec.get("basePath")

    if host is None or base_path is None:
        raise ValueError("host and base_path are required")

    folders = {}

    for path in paths.keys():
        # 1. Create folder based on path
        normalized_path = path.replace(base_path, "")
        folder_name = normalized_path.split("/")[1]  # /pets/{petId} => pets
        folder_name = normalize_class_name(folder_name)
        if folder_name not in folders:
            folders[folder_name] = {}

        # 2. Create function based on method and add to folder
        for method_name in [k for k in paths[path].keys() if k in METHODS]:
            method = paths[path][method_name]
            func = (
                normalize_function_name(method["operationId"])
                if method.get("operationId")
                else normalize_function_name(method["summary"])
            )
            folders[folder_name][func] = {"method": method_name.upper(), "url": build_url(host, base_path, path)}

    return folders


class Swagger(BaseRunner):
    """Instance of a Swagger Spec Runner with executable request functions.

    Args:
        spec_path: The path to the Swagger spec file (.yaml | .yml | .json)
        user_variables: An optional dict of variables to be used by Swagger
        host: The BASE_URL to prepend to all paths in the spec
        base_path: The BASE_PATH to prepend to all paths in the spec

    Example:
        host = "https://api.app.shortcut.com"
        base_path = "/api/v3"

        Request URL for getting an Epic Workflow would then be:
        https://api.app.shortcut.com/api/v3/epic-workflows

    Format:
        Swagger.ExecutableFolder.ExecutableRequest(**kwargs)

    Example:
        # Instantiate a Swagger object
        runner = Swagger(spec_path, user_variables={"USERNAME": "foo", "PASSWORD": "bar"})

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
        user_variables: Optional[Dict] = None,
        host: Optional[str] = None,
        base_path: Optional[str] = None,
    ):
        super().__init__(spec_path, user_variables)
        self.host = host
        self.base_path = base_path
        self.folders = self.__load()

    def __load(self):
        reqs = find_requests(self.spec, host=self.host, base_path=self.base_path)
        return base.map_requests_to_executable_functions(reqs, self.variables)
