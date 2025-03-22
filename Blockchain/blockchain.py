from Blockchain.block import Block
from auxiliary.DButils import DBUtils

class Blockchain:
    def __init__(self):
        self.chain = []
        self.block = Block
        self.db_utils = DBUtils()
        self.db_utils.create_db()
        self.chain = self.db_utils.load_blockchain_from_db(self.block)
        if not self.chain:
            self.create_genesis_block()

    def create_genesis_block(self):
        """Создаёт генезис блок."""
        genesis_block = self.block(index=1, previous_hash="0", data="Genesis Block")
        self.chain.append(genesis_block)
        self.db_utils.save_block_in_db(genesis_block)

    def add_block(self, data, file_data=None):
        """Создание нового блока."""
        previous_block = self.chain[-1]  # Последний блок в цепочке
        new_block = self.block(
            index=len(self.chain) + 1,
            previous_hash=previous_block.hash,  # Используем хэш предыдущего блока
            data=data,
            file_data=file_data
        )
        self.chain.append(new_block)
        self.db_utils.save_block_in_db(new_block)

    def is_chain_valid(self):
        """Проверка целостности цепочки."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Вычисляем хэш текущего блока
            calculated_hash = current_block.calculate_hash()
            if current_block.hash != calculated_hash:
                print(f"Invalid hash for block {current_block.index}")
                print(f"Stored hash: {current_block.hash}")
                print(f"Calculated hash: {calculated_hash}")
                return False

            # Проверяем связь с предыдущим блоком
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash for block {current_block.index}")
                print(f"Expected previous hash: {previous_block.hash}")
                print(f"Actual previous hash: {current_block.previous_hash}")
                return False
        return True