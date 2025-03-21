import sqlite3
import datetime
from Blockchain.block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.block = Block
        self.create_db()
        self.load_blockchain_from_db()
        if not self.chain:
            self.create_genesis_block()

    def create_genesis_block(self):
        """Создаёт генезис блок"""
        genesis_block = self.block(index=1, previous_hash="0", data="Genesis Block")
        self.chain.append(genesis_block)
        self.save_block_in_db(genesis_block)

    def add_block(self, data, file_data=None):
        """Создание нового блока"""
        previous_block = self.chain[-1]  # Последний блок в цепочке
        new_block = self.block(
            index=len(self.chain) + 1,
            previous_hash=previous_block.hash,  # Используем хэш предыдущего блока
            data=data,
            file_data=file_data
        )
        self.chain.append(new_block)
        self.save_block_in_db(new_block)

    def is_chain_valid(self):
        """Проверка целостности цепочки"""
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

    def create_db(self):
        """Создаёт базу данных"""
        with sqlite3.connect("blockchain.db") as con:
            cur = con.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS Blocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hash TEXT,
                    previous_hash TEXT,
                    data TEXT,
                    file_data TEXT,
                    time REAL
                )
            ''')
            con.commit()

    def load_blockchain_from_db(self):
        """Загрузка из базы данных"""
        with sqlite3.connect("blockchain.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Blocks ORDER BY id")
            rows = cur.fetchall()

            self.chain = []
            for row in rows:
                block = self.block(
                    index=row[0],
                    previous_hash=row[2],
                    data=row[3],
                    file_data=row[4],
                    timestamp=row[5]
                )
                block.hash = row[1]
                self.chain.append(block)

    def save_block_in_db(self, block):
        """Сохранение блока в базе данных"""
        with sqlite3.connect("blockchain.db") as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO Blocks (hash, previous_hash, data, file_data, time)
                VALUES (?, ?, ?, ?, ?)
            """, (block.hash, block.previous_hash, str(block.data), block.file_data, block.timestamp))
            con.commit()

    def print_chain(self):
        """Вывод информации о всех блоках в цепочке"""
        for block in self.chain:
            unix_time = block.timestamp
            normal_time = datetime.datetime.fromtimestamp(unix_time)
            print(f"Block {block.index}:")
            print(f"  Hash: {block.hash}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Data: {block.data}")
            print(f"  File Data: {block.file_data}")
            print(f"  Timestamp: {normal_time}")
            print("-" * 40)