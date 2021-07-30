from typing import Dict
import os
import json
import requests
from pyclinic.models.postman_collection_model import PostmanCollection


def _preprocess_postman_collection(collection: Dict) -> Dict:
    if collection["item"][0].get("item") is None:
        # no folders, just items
        pass
    else:
        # rename "item" to "folders"
        collection["folders"] = collection.pop("item")
    return collection


def load_postman_collection_from_str(json_str: str) -> PostmanCollection:
    collection = json.loads(json_str)
    collection = _preprocess_postman_collection(collection)
    return PostmanCollection(**collection)


def load_postman_collection_from_url(collection_url: str) -> PostmanCollection:
    response = requests.get(collection_url)
    if not response.ok:
        raise ValueError(f"Unable to get postman collection from url: {collection_url}")

    collection = _preprocess_postman_collection(response.json())
    return PostmanCollection(**collection)


def load_postman_collection_from_file(collection_file_path: str) -> PostmanCollection:
    try:
        with open(collection_file_path, "r") as f:
            collection = load_postman_collection_from_str(f.read())
    except FileNotFoundError:
        raise ValueError(f"Unable to find or open file: {collection_file_path}")
    return collection


def find_response_bodies(collection: PostmanCollection) -> Dict:
    bodies = {}
    if collection.folders is not None:
        for folder in collection.folders:
            bodies[folder.name] = {}
            for item in folder.item:
                bodies[folder.name][item.name] = []
                for response in item.response:
                    if type(response.body) is str and response.body != "":
                        bodies[folder.name][item.name].append(json.loads(response.body))
                    else:
                        bodies[folder.name][item.name].append(response.body)
    else:
        for item in collection.item:
            bodies[item.name] = []
            for response in item.response:
                if type(response.body) is str and response.body != "":
                    bodies[item.name].append(json.loads(response.body))
                else:
                    bodies[item.name].append(response.body)
    return bodies


def write_model_to_file(filename: str, model: str):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            contents = f.read()

        with open(filename, "a") as f:
            for line in model.split("\n"):
                if (
                    line not in contents
                    or line.startswith("class")
                    or line.startswith(" ")
                ):
                    f.write(line + "\n")
    else:
        with open(filename, "w") as f:
            f.write(model)
