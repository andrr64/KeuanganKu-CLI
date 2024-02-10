import sqlite3

tableName = 'income_category'
tableData = {
    'id': 'INTEGER PRIMARY KEY',
    'title': 'TEXT NOT NULL'
}
initData = ['Gaji', 'Bonus', 'Uang Saku']

class SQLKategoriPengeluaran:
    def __init__(self):
        pass

    def initTable(self, connection: sqlite3.Connection):
        # Buat tabel jika belum ada
        table_columns = ', '.join([f'{column} {datatype}' for column, datatype in tableData.items()])
        connection.execute(f'CREATE TABLE IF NOT EXISTS {tableName} ({table_columns})')

        # Masukkan data initData ke dalam tabel
        for item in initData:
            connection.execute(f"INSERT INTO {tableName} (title) VALUES ('{item}')")

        # Commit perubahan ke database
        connection.commit()