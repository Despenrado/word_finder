import os
import shutil

import pytest

from app.services.file_services.csv_service import CSVFileService
from app.utils.exceptions import FLException


@pytest.fixture(scope="module")
def temp_dir():
    dir_path = "tests/tmp"
    os.makedirs(dir_path, exist_ok=True)
    yield dir_path

    shutil.rmtree(dir_path)


@pytest.mark.parametrize("file_path, pattern, expected_valid, expected_invalid", [
    ("example.csv", "Quantori", "example_valid.csv", "example_invalid.csv"),
    ("example.csv", "quantori", "example_valid.csv", "example_invalid.csv"),
    ("example.csv", "NotFound", "not_found_valid.csv", "not_found_invalid.csv"),
    ("example.csv", "", "all.csv", "empty_data.csv"),
    ("empty_data.csv", "quantori", "empty_data.csv", "empty_data.csv"),
])
def test_process_file(temp_dir, file_path, pattern, expected_valid, expected_invalid):
    service = CSVFileService(temp_dir, pattern)

    with open(f'tests/data/{file_path}', 'rb') as f:
        _, result_valid_file, result_invalid_file = service._process_file(f.read(), service.search_word)

    assert os.path.exists(result_valid_file[(len('file://')):])
    assert os.path.exists(result_invalid_file[(len('file://')):])
    with (open(f'tests/data/{expected_valid}', 'rb') as expected,
          open(result_valid_file[(len('file://')):], 'rb') as result):
        assert expected.read() == result.read()
    with (open(f'tests/data/{expected_invalid}', 'rb') as expected,
          open(result_invalid_file[(len('file://')):], 'rb') as result):
        assert expected.read() == result.read()


@pytest.mark.parametrize("file_path, pattern", [
    ("empty.csv", "quantori"),
])
def test_process_file_exception(temp_dir, file_path, pattern):
    service = CSVFileService(temp_dir, pattern)

    with pytest.raises(FLException):
        with open(f'tests/data/{file_path}', 'rb') as f:
            _, result_valid_file, result_invalid_file = service._process_file(f.read(), service.search_word)


@pytest.mark.parametrize("row, column_name, expected", [
    (["Company Name", "Address", "Phone"], "Company Name", 0),
    (["Phone", "Address", "Company Name"], "Company Name", 2),
])
def test_get_column_index(row, column_name, expected):
    service = CSVFileService("temp", "temp")
    assert service._get_column_index(row, column_name) == expected


@pytest.mark.parametrize("row, column_name", [
    (["Phone", "Address", "Company Name"], "Not Found"),
    ([], "Not Found"),
])
def test_get_column_index_exception(row, column_name):
    service = CSVFileService("temp", "temp")
    with pytest.raises(FLException):
        service._get_column_index(row, column_name)


@pytest.mark.parametrize(
    "rows, valid_column_index, pattern, expected_has_valid_rows, expected_valid_rows, expected_invalid_rows",
    [
        # All valid rows
        (
            [["Quantori", "Address Q", "Phone Q"],
             ["Google", "Address B", "Phone B"],
             ["Microsoft", "Address C", "Phone C"]],
            0,
            "quantori",
            True,
            [["Quantori", "Address Q", "Phone Q"]],
            []
        ),
        # Some rows are valid, some are invalid
        (
            [["Quantori", "Address Q", "Phone Q"],
             ["Invalid G", "Quantori", "Phone G"],
             ["Invalid M", "Address M", "Microsoft"]],
            0,
            "quantori",
            True,
            [["Quantori", "Address Q", "Phone Q"]],
            [["Invalid G", "Quantori", "Phone G"]]
        ),
        # No matches at all
        (
            [["Invalid A", "Address A", "Phone A"],
             ["Invalid B", "Address B", "Phone B"]],
            0,
            "quantori",
            False,
            [],
            []
        ),
        # Empty rows
        (
            [],
            0,
            "quantori",
            False,
            [],
            []
        ),
        # Case-insensitive matching
        (
            [["QuanTori", "Address A", "Phone A"],
             ["GOOGLE", "AddressG", "Phone G"],
             ["microsoft", "Address M", "Phone M"]],
            0,
            "quantori",
            True,
            [["QuanTori", "Address A", "Phone A"]],
            []
        ),
        # multiple words
        (
            [["Quantoriiiii", "Address Q", "Phone Q"],
             ["GOOGLE", "Address G", "Phone G"],
             ["microsoft", "Address M", "Phone M"]],
            0,
            "quantori",
            True,
            [["Quantoriiiii", "Address Q", "Phone Q"]],
            []
        )
    ]
)
def test_process_rows(rows, valid_column_index, pattern, expected_has_valid_rows, expected_valid_rows, expected_invalid_rows):
    service = CSVFileService("temp", pattern)
    has_valid_rows, valid_rows, invalid_rows = service._process_rows(rows, valid_column_index, pattern)

    assert has_valid_rows == expected_has_valid_rows
    assert valid_rows == expected_valid_rows
    assert invalid_rows == expected_invalid_rows