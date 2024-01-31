import sqlite3
from database.model.expense import ModelExpense

tableName = 'expense'
tableData = {
    'id' : 'INTEGER PRIMARY KEY',
    'title': 'TEXT NOT NULL',
    'time': 'TEXT NOT NULL',
    'amount': 'REAL NOT NULL',
    'category_id' : 'INTEGER NOT NULL',
    'rate' : 'INTEGER NOT NULL'
}

class SQLExpense:
    def __init__(self):
        pass

    def initTable(self, connection: sqlite3.Connection):
        # Buat tabel jika belum ada
        table_columns = ', '.join([f'{column} {datatype}' for column, datatype in tableData.items()])
        connection.execute(f'CREATE TABLE IF NOT EXISTS {tableName} ({table_columns})')

        # Commit perubahan ke database
        connection.commit()

    def read_all(self, connection: sqlite3.Connection):
        '''Return list of all expenses (None if empty)'''
        cursor = connection.execute(f'SELECT * FROM {tableName}')
        rows = cursor.fetchall()
        cursor.close()
        if len(rows) == 0:
            return None
        expenseList = []
        for data in rows:
            expenseList.append(ModelExpense(*data))
        return expenseList

    def read_id(self, connection: sqlite3.Connection, expense_id: int):
        '''Read expense data by id'''
        cursor = connection.execute(f'SELECT * FROM {tableName} WHERE id = ?', (expense_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is not None:
            return ModelExpense(*row)
        return None

    def insert(self, connection: sqlite3.Connection, data: ModelExpense):
        '''Insert expense data into the database'''
        try:
            columns = ', '.join(data.__annotations__.keys())
            values = ', '.join(['?' for _ in data.__annotations__.keys()])
            query = f'INSERT INTO {tableName} ({columns}) VALUES ({values})'

            connection.execute(query, ModelExpense.toJson(data))
            connection.commit()
            return True
        except sqlite3.Error:
            connection.rollback()
            return False

    def update(self, connection: sqlite3.Connection, data: ModelExpense):
        '''Update expense data in the database'''
        try:
            set_clause = ', '.join([f'{key} = ?' for key in data.__annotations__.keys()])
            query = f'UPDATE {tableName} SET {set_clause} WHERE id = ?'
            connection.execute(query, list(data.__dict__.values()) + [data.id])
            connection.commit()
            return True
        except sqlite3.Error:
            connection.rollback()
            return False

    def delete(self, connection: sqlite3.Connection, expense_id: int):
        '''Delete expense data from the database'''
        try:
            connection.execute(f"DELETE FROM {tableName} WHERE id = ?", (expense_id,))
            connection.commit()
            return True
        except sqlite3.Error:
            connection.rollback()
            return False