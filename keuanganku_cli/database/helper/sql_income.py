import sqlite3
tableName = 'income'
tableData = {
    'id' : 'INTEGER PRIMARY KEY',
    'title': 'TEXT NOT NULL',
    'time': 'INTEGER NOT NULL',
    'amount': 'REAL NOT NULL',
    'category_id' : 'INTEGER NOT NULL',
}

class SQLPemasukan:
    def __init__(self):
        pass

    def initTable(self, connection : sqlite3.Connection):
        # Buat tabel jika belum ada
        table_columns = ', '.join([f'{column} {datatype}' for column, datatype in tableData.items()])
        connection.execute(f'CREATE TABLE IF NOT EXISTS {tableName} ({table_columns})')

        # Commit perubahan ke database
        connection.commit()