from typing import Tuple, Optional

from fastapi import UploadFile

from app.services.file_services.base_service import BaseFileService, serialize_result, deserialize_result
from app.utils.cache import cache
from app.utils.md5 import calculate_md5_from_data_and_pattern


class TXTFileService(BaseFileService):
    def __init__(self, search_word, chunk_size=1024 * 1024):
        super().__init__(search_word)
        self.chunk_size = chunk_size # default 1Mb


    def process_file(self, file: UploadFile) -> Tuple[bool, Optional[str], Optional[str]]:
        buffer = b''
        found = False

        while chunk := file.file.read(self.chunk_size):
            chunk = buffer + chunk

            if self._is_pattern_exists(chunk, self.search_word):
                found = True
                break

            buffer = chunk[-(len(self.search_word) - 1):]

        return found, None, None


    @cache(key_func=calculate_md5_from_data_and_pattern, serializer=serialize_result, deserializer=deserialize_result)
    def _is_pattern_exists(self, data, pattern): # Rabin Karp algorithm
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        text = data.lower()

        n = len(text)
        m = len(pattern)
        pattern_hash = hash(pattern)
        subtext_hash = hash(text[:m])

        for i in range(n - m + 1):
            if pattern_hash == subtext_hash and text[i:i + m] == pattern:
                return True

            if i < n - m:
                subtext_hash = hash(text[i+1:i + m +1])

        return False

