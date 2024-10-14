import os

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_endpoint_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"


@pytest.mark.parametrize("file_path, expected", [
    ("empty.txt", False),
    ("quantori_lower.txt", True),
    ("quantori_upper.txt", True),
    ("quantori_only.txt", True),
    ("quantori_not_exists.txt", False),
    ("quantori_incorrect.txt", False),
    ("quantori_large_not_exists.txt", False),
    ("quantori_large.txt", True),
    ("quantori_large_chunks.txt", True),
])
def test_upload_txt_file_success(file_path, expected):
    with open(f'./tests/data/{file_path}', "rb") as file:
        files = {"file": (file_path, file, "text/plain")}
        response = client.post("/api/upload", files=files)

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/html")

    if expected:
        assert '<p><strong>Word "Quantori" exists:</strong> True</p>' in response.text
    else:
        assert '<p><strong>Word "Quantori" exists:</strong> False</p>' in response.text


@pytest.mark.parametrize("file_path, expected", [
    ("example.csv", True),
])
def test_upload_csv_file_success(file_path, expected):
    with open(f'./tests/data/{file_path}', "rb") as file:
        files = {"file": (file_path, file, "text/csv")}
        response = client.post("/api/upload", files=files)

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/html")

    if expected:
        assert '<p><strong>Word "Quantori" exists:</strong> True</p>' in response.text
        assert '<p>Valid File<a href="file://' in response.text
        assert '<p>Invalid File<a href="file://' in response.text
    else:
        assert '<p><strong>Word "Quantori" exists:</strong> False</p>' in response.text


@pytest.mark.parametrize("file_path, expected", [
    ("example.xlsx", True),
])
def test_upload_xlsx_file_success(file_path, expected):
    with open(f'./tests/data/{file_path}', "rb") as file:
        files = {"file": (file_path, file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        response = client.post("/api/upload", files=files)

    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/html")

    if expected:
        assert '<p><strong>Word "Quantori" exists:</strong> True</p>' in response.text
        assert '<p>Valid File<a href="file://' in response.text
        assert '<p>Invalid File<a href="file://' in response.text
    else:
        assert '<p><strong>Word "Quantori" exists:</strong> False</p>' in response.text