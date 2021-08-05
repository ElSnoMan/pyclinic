import re


def normalize_function_name(name: str) -> str:
    string = re.sub(r"[?!@#$%^&*()_\-+=,./\'\\\"|:;{}\[\]]", " ", name)
    return "_".join(string.lower().split())


def normalize_class_name(string):
    string = re.sub(r"[?!@#$%^&*()_\-+=,./\'\\\"|:;{}\[\]]", " ", string)
    return string.title().replace(" ", "")
