import sqlite3
from database.model.model_expense_category import ModelExpenseCategory

tableName = 'expense_category'
tableData = {
    'id': 'INTEGER PRIMARY KEY',
    'title': 'TEXT NOT NULL'
}
initData = [
    'Makanan dan Minuman Primer',
    'Makanan dan Minuman Sekunder',
    'Gaya Hidup',
    'Transportasi',
    'Perawatan Kendaraan',
    'Hutang'
]

class SQLExpenseCategory:
    def __init__(self):
        pass

    def read_id(self, db: sqlite3.Connection, category_id: int) -> (ModelExpenseCategory | None):
        '''Read expense category data by id'''
        cursor = db.execute(f'SELECT * FROM {tableName} WHERE id = ?', (category_id,))
        row = cursor.fetchone()
        cursor.close()
        if len(row) != 0:
            return ModelExpenseCategory(id=row[0], title=row[1])
        return None

    def readAll(self, db: sqlite3.Connection):
        '''Return list of expense category (None if empty)'''
        cursor = db.execute(f'SELECT * FROM {tableName}')
        rows = cursor.fetchall()
        cursor.close()
        if len(rows) == 0:
            return None
        categoryList = []
        for data in rows:
            categoryList.append(
                ModelExpenseCategory(
                    id=data[0],
                    title=data[1]
                )
            )
        return categoryList

    def update(self, db: sqlite3.Connection, data: ModelExpenseCategory) -> bool:
            '''Update expense category data in the database'''
            try:
                db.execute(f"UPDATE {tableName} SET judul = ? WHERE id = ?", (data.title, data.id))
                db.commit()
                return True
            except sqlite3.Error:
                db.rollback()
                return False

    def delete(self, db: sqlite3.Connection, data: ModelExpenseCategory) -> bool:
        '''Delete expense category data from the database'''
        try:
            db.execute(f"DELETE FROM {tableName} WHERE id = ?", (data.id,))
            db.commit()
            return True
        except sqlite3.Error:
            db.rollback()
            return False

    def insert(self, db: sqlite3.Connection, data: ModelExpenseCategory):
        '''Insert expense category data into the database'''
        db.execute(f"INSERT INTO {tableName} (judul) VALUES (?)", (data.title,))
        db.commit()

    def initTable(self, connection: sqlite3.Connection):
        # Buat tabel jika belum ada
        table_columns = ', '.join([f'{column} {datatype}' for column, datatype in tableData.items()])
        connection.execute(f'CREATE TABLE IF NOT EXISTS {tableName} ({table_columns})')

        # Masukkan data initData ke dalam tabel
        for item in initData:
            connection.execute(f"INSERT INTO {tableName} (title) VALUES ('{item}')")

        # Commit perubahan ke database
        connection.commit()