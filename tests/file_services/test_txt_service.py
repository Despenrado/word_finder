import pytest
from fastapi import UploadFile
from io import BytesIO

from app.services.file_services.txt_service import TXTFileService


@pytest.mark.parametrize("file_path, pattern, expected", [
    ("empty.txt", "Quantori", False),
    ("quantori_lower.txt", "Quantori", True),
    ("quantori_upper.txt", "Quantori", True),
    ("quantori_only.txt", "Quantori", True),
    ("quantori_not_exists.txt", "Quantori", False),
    ("quantori_incorrect.txt", "Quantori", False),
])
def test_is_pattern_exists(file_path, pattern, expected):
    with open(f'./tests/data/{file_path}', 'r') as f:
        data = f.read()
        service = TXTFileService(pattern)
        assert service._is_pattern_exists(data, service.search_word) == expected


@pytest.mark.parametrize("file_path, pattern, expected", [
    ("empty.txt", "Quantori", False),
    ("quantori_lower.txt", "Quantori", True),
    ("quantori_upper.txt", "Quantori", True),
    ("quantori_only.txt", "Quantori", True),
    ("quantori_not_exists.txt", "Quantori", False),
    ("quantori_incorrect.txt", "Quantori", False),
    ("quantori_large_not_exists.txt", "Quantori", False),
    ("quantori_large.txt", "Quantori", True),
    ("quantori_large_chunks.txt", "Quantori", True),
])
def test_process_file(file_path, pattern, expected):
    with open(f'./tests/data/{file_path}', 'rb') as f:
        upload_file = UploadFile(filename=file_path, file=BytesIO(f.read()))
        service = TXTFileService(pattern, 1024 * 100)
        result, _, _ =service.process_file(upload_file)
        assert result == expected