import sqlite3
tableName = 'pengeluaran'
tableData = {
    'id' : 'INTEGER PRIMARY KEY',
    'judul': 'TEXT NOT NULL',
    'waktu': 'TEXT NOT NULL',
    'jumlah': 'REAL NOT NULL',
    'id_kategori' : 'INTEGER NOT NULL',
    'rating' : 'INTEGER NOT NULL'
}

class SQLPengeluaran:
    def __init__(self):
        pass

    def initTable(self, connection : sqlite3.Connection):
        # Buat tabel jika belum ada
        table_columns = ', '.join([f'{column} {datatype}' for column, datatype in tableData.items()])
        connection.cursor.execute(f'CREATE TABLE IF NOT EXISTS ${tableName} ({table_columns})')

        # Commit perubahan ke database
        connection.commit()