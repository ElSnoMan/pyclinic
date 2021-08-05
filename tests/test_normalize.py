import pytest
from pyclinic.normalize import normalize_function_name, normalize_class_name


FUNCTION_NAME_EXAMPLES = [
    ("Is 10 Even?", "is_10_even"),
    ("{get order}", "get_order"),
]


@pytest.mark.parametrize("function_name, expected", FUNCTION_NAME_EXAMPLES)
def test_normalize_function_names(function_name, expected):
    assert normalize_function_name(function_name) == expected


FOLDER_NAME_EXAMPLES = [
    ("pets", "Pets"),
    ("/{get order}", "GetOrder"),
]


@pytest.mark.parametrize("folder_name, expected", FOLDER_NAME_EXAMPLES)
def test_normalize_folder_names(folder_name, expected):
    assert normalize_class_name(folder_name) == expected
