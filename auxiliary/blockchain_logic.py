from Blockchain.blockchain import Blockchain
import base64
import datetime

class BlockchainLogic:
    def __init__(self):
        self.blockchain = Blockchain()

    def add_block(self, data, file_path=None):
        file_data = None
        if file_path:
            with open(file_path, 'rb') as file:
                file_data = base64.b64encode(file.read()).decode('utf-8')
        if data or file_data:
            self.blockchain.add_block(data, file_data)

    def get_chain(self):
        return self.blockchain.chain

    def is_chain_valid(self):
        return self.blockchain.is_chain_valid()

    def get_block_info(self, block):
        unix_time = block.timestamp
        normal_time = datetime.datetime.fromtimestamp(unix_time)
        info = (
            f"Индекс блока: {block.index}\n"
            f"Хэш блока: {block.hash}\n"
            f"Хэш предыдущего блока: {block.previous_hash}\n"
            f"Данные: {block.data}\n"
            f"Время создания: {normal_time}"
        )
        if block.file_data:
            info += "\nФайл: Присутствует"
        else:
            info += "\nФайл: Отсутствует"
        return info

    def download_file(self, block, save_path):
        if block.file_data:
            file_data = base64.b64decode(block.file_data.encode('utf-8'))
            with open(save_path, 'wb') as file:
                file.write(file_data)
            return True
        return False