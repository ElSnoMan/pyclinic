import os
import re
import json
import logging
from typing import Dict, List, Optional, Tuple
import yaml
import requests
from rich.console import Console
from pyclinic.normalize import normalize_class_name, normalize_function_name


console = Console()
_logger = logging.getLogger(__name__)


METHODS = [
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "head",
    "options",
    "trace",
]


def load_openapi_spec_from_file(path) -> Dict:
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, "r") as f:
        if path.endswith(".yaml") or path.endswith(".yml"):
            return yaml.load(f, Loader=yaml.FullLoader)

        elif path.endswith(".json"):
            return json.load(f)

        else:
            raise ValueError("Unsupported file format: {}".format(path))


def extract_base_url_from_spec(spec: Dict) -> Tuple[str, Dict]:
    """Extract the server urls from the spec to be used when generating functions.

    Args:
        spec: The OpenAPI Spec dictionary to extract the urls from.

    Returns:
        A tuple of the first BASE_URL (as default) and a variables dictionary that sets the BASE_URL.

    Exceptions:
        ValueError: If the spec has no URLs in its "servers" section.
    """
    if len(spec["servers"]) == 0:
        raise ValueError("No server URLs found in spec")

    base_urls = [s["url"] for s in spec["servers"]]
    variables = {"BASE_URL": base_urls[0]}
    return base_urls[0], variables


def find_requests(spec: Dict) -> Dict:
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
    url, _ = extract_base_url_from_spec(spec)
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


def build_request_to_send(request: Dict, variables: Dict) -> Dict:
    """
    request looks like:
    {
        "method": "GET",
        "url": "{BASE_URL}/Accounts/v1",
        "headers": {"Authorization": "Bearer {token}"},
    }
    """
    OPENAPI_VARIABLE = r"\{([^}]+)\}"  # {variable}
    for key, value in request.items():
        for found_var in re.findall(OPENAPI_VARIABLE, string=str(value)):
            found_value = variables.get(found_var)
            if found_value is None:
                _logger.warning(f"Variable {{{found_var}}} was not found in the Variables provided")
            else:
                request[key] = value.replace("{" + found_var + "}", str(found_value))
    return request


class OpenApiExecutableRequest:
    def __init__(self, name: str, request: Dict):
        self.name = name
        self.request = request

    def __call__(self, variables: Dict = None, **kwargs):
        if kwargs:
            self.request.update(kwargs)
        if variables:
            self.request = build_request_to_send(self.request, variables)
        response = requests.request(**self.request)
        return response

    def help(self):
        print(), console.rule(f"[bold green]Request to Send for {self.name}[/bold green]")
        console.print(self.request)


class OpenApiFolder:
    def __init__(self, folder_name: str, folder: Dict[str, OpenApiExecutableRequest]):
        """A flat dictionary with request names as keys and their executables as the values."""
        self.name = folder_name
        self.folder = folder

    def __getattr__(self, name):
        if name not in self.folder:
            available_requests = "\n".join(self.folder.keys())
            raise ValueError(
                f"{self.name} Folder doesn't have a request with the operationId of: {name}\n\nDid you mean any of these:\n\n{available_requests}"
            )
        return self.folder[name]

    def help(self) -> List[str]:
        """Display all of the executable functions within this folder."""
        print(), console.rule(f"[bold green]Requests in {self.name} Folder[/bold green]")

        if len(self.folder) == 0:
            console.print("No functions found!", style="bold red")
            return

        keys = [key for key in self.folder.keys()]
        for i, key in enumerate(keys):
            console.print(f"{str(i+1):5s} [light_sky_blue1]{key}[/light_sky_blue1]", style="white")
        console.print("\nExample Usage", style="bold u gold1")
        console.print(f"\nresponse = runner.{self.name}.{keys[-1]}()")
        return keys


def map_requests_to_executable_functions(folders: Dict, variables: Dict) -> Dict:
    """Map requests to executable functions to be used by OpenApi runner.

    Returns a Dict like:
    {
        "Pets": OpenApiFolder({
            "list_all_pets": OpenApiExecutableRequest(request_to_send),
            "create_a_pet": OpenApiExecutableRequest(request_to_send),
        }),
        "PetId": OpenApiFolder({
            "info_for_a_pet": OpenApiExecutableRequest(request_to_send)
        }),
    }

    runner = OpenApiRunner(spec_path, variables)
    runner.Pets.list_all_pets()
    runner.PetId.info_for_a_pet(pet_id)
    """
    for folder_name in folders.keys():
        folder = folders[folder_name]
        for request_name in folder.keys():
            request = build_request_to_send(folder[request_name], variables)
            folder[request_name] = OpenApiExecutableRequest(request_name, request)
        folders[folder_name] = OpenApiFolder(folder_name, folder)
    return folders


class OpenApi:
    """Instance of a OpenAPI Spec Runner with executable request functions.

    Args:
        spec_path: The path to the OpenApi spec file (.yaml | .yml | .json)
        user_variables: An optional dict of variables to be used by OpenApi

    Format:
        OpenApi.OpenApiFolderRequest.OpenApiExecutableRequest(**kwargs)

    Examples:
        # Instantiate a OpenApi object
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
        user_variables: Optional[Dict] = None,
    ):
        self.spec = load_openapi_spec_from_file(spec_path)
        self.title = self.spec["info"]["title"]
        self.variables = user_variables or {}
        self.folders = self.__load()

    def __load(self):
        reqs = find_requests(self.spec)
        return map_requests_to_executable_functions(reqs, self.variables)

    def __getattr__(self, name):
        if name not in self.folders:
            available_folders = "\n".join(self.folders.keys())
            raise ValueError(
                f"Spec doesn't have a folder named: {name}\n\nDid you mean any of these:\n\n{available_folders}"
            )
        folder = self.folders[name]
        return folder

    def show_folders(self):
        """Display all folders and functions found in this Spec file."""
        print(), console.rule(f"[bold green]Folders in {self.title}[/bold green]")

        if len(self.folders) == 0:
            console.print("No folders found!", style="bold red")
            return

        folder_names = list(self.folders.keys())
        for folder_name in folder_names:
            display = f"\n{folder_name}." if folder_name != "Root" else "\n*Root."
            console.print(display, style="bold light_green")
            for request_name in sorted(self.folders[folder_name].folder.keys()):
                console.print(f"\t{request_name}", style="light_sky_blue1")

        example_folder = folder_names[-1]
        example_function = list(self.folders[example_folder].folder.keys())[-1]
        console.print("\nExample Usage", style="bold u gold1")
        console.print(f"\nresponse = runner.{example_folder}.{example_function}()")

    def show_variables(self):
        """Display all variables that this instance of Postman was instantiated with."""
        print(), console.rule(f"[bold green]User Variables for {self.title}[/bold green]")
        console.print(self.variables)
