import hashlib

import pytest

from app.utils.md5 import calculate_md5_from_data_and_pattern


@pytest.mark.parametrize("file_path", [
    "empty.txt",
    "quantori_lower.txt",
    "quantori_upper.txt",
    "quantori_only.txt",
    "quantori_not_exists.txt",
    "quantori_incorrect.txt",
])
def test_calculate_md5_from_data_and_pattern_file(file_path):
    with open(f'tests/data/{file_path}', 'rb') as f:
        data = f.read()
        expected_hash = hashlib.md5(data).hexdigest()
        assert calculate_md5_from_data_and_pattern(None, data, None) == expected_hash


def test_calculate_md5_from_data_and_pattern_data_none():
    expected_hash = hashlib.md5(b'').hexdigest()
    assert calculate_md5_from_data_and_pattern(None, None, None) == expected_hash


@pytest.mark.parametrize("text", [
    "Quantori",
    "random-text",
    "",
])
def test_calculate_md5_from_data_and_pattern_text(text):
    expected_hash = hashlib.md5(text.encode()).hexdigest()
    assert calculate_md5_from_data_and_pattern(None, None, text) == expected_hash