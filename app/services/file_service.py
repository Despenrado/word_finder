import os

from fastapi import UploadFile

from app.utils.exceptions import FLException


class FileService:

    def __init__(self, storage_path):
        self.storage_path = storage_path

        if not os.path.exists(storage_path):
            os.makedirs(storage_path)


    def get_file_service(self, filename, word):
        if filename.endswith('.txt'):
            from app.services.file_services.txt_service import TXTFileService
            return TXTFileService(word)
        elif filename.endswith('.csv'):
            from app.services.file_services.csv_service import CSVFileService
            return CSVFileService(self.storage_path, word)
        elif filename.endswith('.xlsx'):
            from app.services.file_services.xlsx_service import XLSXFileService
            return XLSXFileService(self.storage_path, word)
        else:
            raise FLException(status_code=400, message='File type not supported')


    async def process_file(self, file: UploadFile, search_word):
        service = self.get_file_service(file.filename, search_word)
        return service.process_file(file)


    def get_file_path(self, file_name):
        file_path = os.path.join(self.storage_path, file_name)
        if not os.path.exists(file_path):
            raise FLException(status_code=404, message='File not found')
        return file_path
