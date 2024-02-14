import sqlite3
from database.model.model_expense_category import ModelExpenseCategory

tableName = 'expense_category'
tableData = {
    'id': 'INTEGER PRIMARY KEY',
    'title': 'TEXT NOT NULL',
    'active': 'INTEGER NOT NULL'
}
initData = [
    'Primary Food and Beverage',
    'Secondary Food and Beverage',
    'Lifestyle',
    'Transportation',
    'Vehicle Maintenance',
    'Debt'
]

class SQLExpenseCategory:
    def __init__(self):
        pass

    def dyn_readById(self, db: sqlite3.Connection, category_id: int) -> (ModelExpenseCategory | None):
        '''Read expense category data by id'''
        cursor = db.execute(f'SELECT * FROM {tableName} WHERE id = ?', (category_id,))
        row = cursor.fetchone()
        cursor.close()
        if len(row) != 0:
            return ModelExpenseCategory(id=row[0], title=row[1])
        return None

    def ls_readAll(self, db: sqlite3.Connection):
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
                    title=data[1],
                    active=data[2]
                )
            )
        return categoryList

    def b_update(self, db: sqlite3.Connection, data: ModelExpenseCategory) -> bool:
            '''Update expense category data in the database'''
            try:
                db.execute(f"UPDATE {tableName} SET judul = ? WHERE id = ?", (data.title, data.id))
                db.commit()
                return True
            except sqlite3.Error:
                db.rollback()
                return False

    def b_delete(self, db: sqlite3.Connection, data: ModelExpenseCategory) -> bool:
        '''Delete expense category data from the database'''
        try:
            db.execute(f"DELETE FROM {tableName} WHERE id = ?", (data.id,))
            db.commit()
            return True
        except sqlite3.Error:
            db.rollback()
            return False

    def b_insert(self, db: sqlite3.Connection, data: ModelExpenseCategory):
        '''Insert expense category data into the database'''
        try:
            db.execute(f"INSERT INTO {tableName} (title, active) VALUES (?, ?)", (data.title, data.active))
            db.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error occurred: {e}")
            db.rollback()
            return False

    def initTable(self, connection: sqlite3.Connection):
        # Buat tabel jika belum ada
        table_columns = ', '.join([f'{column} {datatype}' for column, datatype in tableData.items()])
        connection.execute(f'CREATE TABLE IF NOT EXISTS {tableName} ({table_columns})')

        # Masukkan data initData ke dalam tabel
        for item in initData:
            connection.execute(f"INSERT INTO {tableName} (title, active) VALUES ('{item}', 1)")

        # Commit perubahan ke database
        connection.commit()