from tests.test_convert_openapi import FILE_TYPES
import pytest
from tests import utils
from pyclinic.openapi import OpenApi

FILE_TYPES = [
    utils.SWAGGER_PETSTORE_YAML,
    utils.SWAGGER_PETSTORE_JSON,
]


@pytest.mark.skip("Swagger is not supported yet")
@pytest.mark.parametrize("file_type", FILE_TYPES)
def test_convert_swagger_file(file_type):
    runner = OpenApi(file_type)
    runner.show_variables()
    runner.show_folders()
