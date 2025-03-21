import hashlib
import time
import base64

class Block:
    def __init__(self, index, previous_hash, data, file_data=None, timestamp=None):
        self.index = index  # Номер блока
        self.previous_hash = previous_hash  # Хэш предыдущего блока
        self.timestamp = timestamp if timestamp is not None else time.time()  # Время создания блока
        self.data = data  # Информация, которая хранится в блоке
        self.file_data = file_data  # Данные файла (если есть)
        self.hash = self.calculate_hash()  # Хэш этого блока

    def calculate_hash(self):
        """Вычисляет хэш блока на основе его данных"""
        block_string = (
            str(self.index) +
            str(self.previous_hash) +
            str(self.timestamp) +
            str(self.data) +
            (str(self.file_data) if self.file_data else "")
        )
        return hashlib.sha256(block_string.encode()).hexdigest()