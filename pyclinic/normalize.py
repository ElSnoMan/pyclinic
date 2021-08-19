""" Normalize strings to Pythonic Syntax

References:
    https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
"""
import re


def remove_special_characters(name: str) -> str:
    """Remove characters that are not part of the Python naming conventions.

    * Folder and File names
    * Class names
    * Function names
    """
    return re.sub(r"[?!@#$%^&*()_\-+=,./\'\\\"|:;{}\[\]]", " ", name)


def camel_to_snake(name: str) -> str:
    """Convert a camelCase name to a snake_case name.

    Example:
        getUserById => get_user_by_id
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def normalize_function_name(name: str) -> str:
    """Turn a name into a pythonic function name.

    Examples:
        Draw Cards => draw_cards
        Is 10 even? => is_10_even
        {findPetsByStatus} => find_pets_by_status
    """
    string = remove_special_characters(name)
    string = camel_to_snake(string)
    string = "_".join(string.split())
    string = string.replace("__", "_")
    return string


def normalize_class_name(name: str) -> str:
    """Turn a name into a pythonic class name.

    Example:
        Folder 1 => Folder1
    """
    string = remove_special_characters(name)
    words = []
    for word in string.split():
        word = word[0].upper() + word[1:]
        words.append(word)

    return "".join(words)
