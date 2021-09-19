""" Base Module for the different runners: Postman, Swagger 2, and OpenAPI 3"""


import json
import logging
import os
import re
from typing import Dict, List, Optional

import requests
import yaml
from rich.console import Console


console = Console()
logger = logging.getLogger("PyClinic Runner")


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


def load_spec_file(path: str) -> Dict:
    """Read a supported spec file and load it as a Python Dictionary.

    * Supported Spec Files: .json | .yaml | .yml

    Args:
        path: The filepath to the spec file.
    """
    logger.debug(f"Loading spec from file: {path}")
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    with open(path, "r") as f:
        if path.endswith(".yaml") or path.endswith(".yml"):
            return yaml.load(f, Loader=yaml.FullLoader)

        elif path.endswith(".json"):
            return json.load(f)

        else:
            raise ValueError("Unsupported file format: {}".format(path))


def build_request_to_send(request: Dict, variables: Dict) -> Dict:
    """Replace placeholders in the request with the values from the given variables.

    Args:
        request: The request to send with placeholders
        variables: The variables to replace the placeholders with

    If the request that's passed in looks like this:
    {
        "method": "GET",
        "url": "{BASE_URL}/Accounts/v1",
        "headers": {"Authorization": "Bearer {token}"},
    }

    Then the variables should look like this:
    {
        "BASE_URL": "https://api.example.com",
        "token": "1234567890"
    }
    """
    SWAGGER_VARIABLE = r"\{([^}]+)\}"  # {variable}
    for key, value in request.items():
        for found_var in re.findall(SWAGGER_VARIABLE, string=str(value)):
            found_value = variables.get(found_var)
            if found_value is None:
                logger.warning(f"Variable {{{found_var}}} was not found in the variables provided")
            else:
                request[key] = value.replace("{" + found_var + "}", str(found_value))
    return request


class ExecutableRequest:
    """A Python function that executes its wrapped Request when called.

    Args:
        variables: A dictionary of variables to replace the placeholders in the request with
        **kwargs: Any additional keyword arguments to pass to the request

    Example:
        response = runner.Pet.get_pet_by_id(pet_id=123)

        .get_pet_by_id() is the ExecutableRequest
    """

    def __init__(self, name: str, global_request: Dict, request: Dict):
        self.name = name
        self.global_request = global_request
        self.request = request
        if global_request:
            self.request.update(global_request)

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


class ExecutableFolder:
    """A Python class that represents a collection of ExecutableRequests

    Args:
        folder_name: The name of the folder
        folder: A dictionary of ExecutableRequests

    Example:
        response = runner.Pet.get_pet_by_id(pet_id=123)

        .Pet is the ExecutableFolder
    """

    def __init__(self, folder_name: str, folder: Dict[str, ExecutableRequest]):
        self.name = folder_name
        self.folder = folder

    def __getattr__(self, name):
        if name not in self.folder:
            available_requests = "\n".join(self.folder.keys())
            raise ValueError(
                f"{self.name} Folder doesn't have request with the summary of: {name}\n\n"
                / f"Did you mean any of these:\n\n{available_requests}"
            )
        return self.folder[name]

    def help(self) -> List[str]:
        """Display all ExecutableRequests (aka functions) within this folder."""
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


def map_requests_to_executable_functions(folders: Dict, global_request: Dict, variables: Dict) -> Dict:
    """Creates the ExecutableFolders and their respective ExecutableRequests for the entire spec file.

    Each specification has their own schema for organizing the requests.
    1. find_requests() and structure them into our "flat folders" dictionary format
    2. Then pass that dictionary as the `folders` argument to this function.

    Example:
        requests = swagger.find_requests(spec, host=HOST, base_path=BASE_PATH)
        folders = map_requests_to_executable_functions(requests, variables)

    Args:
        folders: The requests found from using find_requests()
        global_request: The global request to add to each request
        variables: A dictionary of variables to replace the placeholders in the request with

    Returns:
        A dictionary like:
        {
            "Pets": ExecutableFolder({
                "list_all_pets": ExecutableRequest(request_to_send),
                "create_a_pet": ExecutableRequest(request_to_send),
            }),
            "PetId": ExecutableFolder({
                "info_for_a_pet": ExecutableRequest(request_to_send)
            }),
        }
    """
    for folder_name in folders.keys():
        folder = folders[folder_name]
        for request_name in folder.keys():
            request = build_request_to_send(folder[request_name], variables)
            folder[request_name] = ExecutableRequest(request_name, global_request, request)
        folders[folder_name] = ExecutableFolder(folder_name, folder)
    return folders


class BaseRunner:
    """Instance of a Spec Runner with executable request functions.

    Args:
        spec_path: The path to the spec file (.yaml | .yml | .json)
        global_request: An optional dict to be added to every request. Useful for things like Authorization headers.
        variables: An optional dict of variables to be used by the runner instance

    Format:
        Runner.ExecutableFolder.ExecutableRequest()

    Examples:
        # Instantiate a Runner object
        runner = Runner(
            spec_path,
            global_request={"headers": {"Authorization": "Bearer {token}"}},
            user_variables={"USERNAME": "foo", "PASSWORD": "bar"}
        )

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
        global_request: Dict = None,
        variables: Optional[Dict] = None,
    ):
        self.spec = load_spec_file(spec_path)
        self.title = self.spec["info"]["title"]
        self.global_request = global_request or dict()
        self.variables = variables or dict()
        self.folders = self.__load()

    def __load(self) -> Dict:
        """Implement the __load() and find_requests() function for each specification runner/wrapper."""
        return dict()

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
        """Display all variables that this Runner instance was instantiated with."""
        print(), console.rule(f"[bold green]User Variables for {self.title}[/bold green]")
        console.print(self.variables)
