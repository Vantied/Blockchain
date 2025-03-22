import sqlite3

class DBUtils:
    def __init__(self, db_name="blockchain.db"):
        self.db_name = db_name

    def create_db(self):
        """Создаёт базу данных и таблицу Blocks, если она не существует."""
        with sqlite3.connect(self.db_name) as con:
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

    def load_blockchain_from_db(self, block_class):
        """Загружает блокчейн из базы данных."""
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Blocks ORDER BY id")
            rows = cur.fetchall()

            chain = []
            for row in rows:
                block = block_class(
                    index=row[0],
                    previous_hash=row[2],
                    data=row[3],
                    file_data=row[4],
                    timestamp=row[5]
                )
                block.hash = row[1]
                chain.append(block)
            return chain

    def save_block_in_db(self, block):
        """Сохраняет блок в базе данных."""
        with sqlite3.connect(self.db_name) as con:
            cur = con.cursor()
            cur.execute("""
                INSERT INTO Blocks (hash, previous_hash, data, file_data, time)
                VALUES (?, ?, ?, ?, ?)
            """, (block.hash, block.previous_hash, str(block.data), block.file_data, block.timestamp))
            con.commit()