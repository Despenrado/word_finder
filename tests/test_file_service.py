import os
import shutil

import pytest

from app.services.file_service import FileService
from app.utils.exceptions import FLException


@pytest.fixture(scope="module")
def temp_dir():
    dir_path = "tests/tmp"
    os.makedirs(dir_path, exist_ok=True)
    yield dir_path

    shutil.rmtree(dir_path)


def test_get_file_service_unsupported_type(temp_dir):
    with pytest.raises(FLException):
        FileService(temp_dir).get_file_service("test_file.xyz", "test_word")


@pytest.mark.parametrize("filename, expected_service_class", [
    ("test_file.txt", "TXTFileService"),
    ("test_file.csv", "CSVFileService"),
    ("test_file.xlsx", "XLSXFileService"),
])
def test_get_file_service_valid_file_types(temp_dir, filename, expected_service_class):
    service_instance = FileService(temp_dir).get_file_service(filename, "test_word")

    assert service_instance.__class__.__name__ == expected_service_class