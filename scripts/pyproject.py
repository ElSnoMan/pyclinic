import os
import toml


def get_version() -> str:
    path = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
    config = toml.load(path)
    version = config["tool"]["poetry"]["version"]
    return version


if __name__ == "__main__":
    print(get_version())
