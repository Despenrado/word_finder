import csv
import os.path
import uuid
from typing import Tuple, Optional

from fastapi import UploadFile

from app.services.file_services.base_service import (
    BaseFileService,
    serialize_result,
    deserialize_result,
)
from app.utils.cache import cache
from app.utils.exceptions import FLException
from app.utils.md5 import calculate_md5_from_data_and_pattern


class CSVFileService(BaseFileService):
    def __init__(self, storage_path, search_word):
        super().__init__(search_word)
        self.storage_path = storage_path

    def _get_column_index(self, row, column_name):
        try:
            return row.index(column_name)
        except ValueError:
            FLException(status_code=400, message='Column "Company Name" not found')

    def _save_rows_to_file(self, headers, rows, file_name):
        file_path = os.path.join(self.storage_path, f"{file_name}.csv")
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            if rows:
                writer.writerows(rows)
        return f"file://{os.path.abspath(file_path)}"

    def process_file(
        self, file: UploadFile
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        contents = file.file.read()
        return self._process_file(contents, self.search_word)

    @cache(
        key_func=calculate_md5_from_data_and_pattern,
        serializer=serialize_result,
        deserializer=deserialize_result,
    )
    def _process_file(self, data, pattern):
        reader = csv.reader(data.decode("utf-8").splitlines())

        headers = next(reader)
        rows = list(reader)

        valid_column_index = self._get_column_index(headers, "Company Name")
        is_word_found, valid_rows, invalid_rows = self._process_rows(
            rows, valid_column_index, pattern
        )

        file_uuid = uuid.uuid4()
        output_valid_file = self._save_rows_to_file(
            headers, valid_rows, f"valid_{file_uuid}"
        )
        output_invalid_file = self._save_rows_to_file(
            headers, invalid_rows, f"invalid_{file_uuid}"
        )

        return is_word_found, output_valid_file, output_invalid_file

    def _process_rows(self, rows, valid_column_index, pattern):
        valid_rows = []
        invalid_rows = []

        for row in rows:
            if pattern in row[valid_column_index].lower():
                valid_rows.append(row)
            else:
                is_in_invalid_column = any(
                    pattern in str(value or "").lower()
                    for i, value in enumerate(row)
                    if i != valid_column_index
                )
                if is_in_invalid_column:
                    invalid_rows.append(row)

        return bool(valid_rows), valid_rows, invalid_rows
