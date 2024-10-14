import json
from abc import ABC, abstractmethod
from typing import Tuple, Optional

from fastapi import UploadFile


class BaseFileService(ABC):
    def __init__(self, search_word):
        self.search_word = search_word.lower()

    @abstractmethod
    def process_file(
        self, file: UploadFile
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        pass


def serialize_result(valid_rows, output_valid_file=None, output_invalid_file=None):
    data = {"valid_rows": bool(valid_rows)}
    if output_valid_file:
        data["output_valid_file"] = output_valid_file
    if output_invalid_file:
        data["output_invalid_file"] = output_invalid_file
    return json.dumps(data)


def deserialize_result(json_data):
    data = json.loads(json_data)
    return (
        bool(data.get("valid_rows", False)),
        data.get("output_valid_file", None),
        data.get("output_invalid_file", None),
    )
