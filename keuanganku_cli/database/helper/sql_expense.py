import sqlite3
from database.model.model_expense import ModelExpense
from database.helper.sql_expense_category import SQLExpenseCategory

from datetime import datetime, timedelta

tableName = 'expense'
tableData = {
    'id' : 'INTEGER PRIMARY KEY',
    'title': 'TEXT NOT NULL',
    'time': 'INTEGER NOT NULL',
    'amount': 'REAL NOT NULL',
    'category_id' : 'INTEGER NOT NULL',
    'rate' : 'INTEGER NOT NULL'
}

class SQLExpense:
    _insertColumnData = ['title', 'time', 'amount', 'category_id', 'rate']
    _insertColumnLength = len(_insertColumnData)

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
            # 4 = category_id
            categoryData = SQLExpenseCategory().read_id(connection, data[4])
            expenseList.append(ModelExpense.fromTuple(data, categoryData))
        return expenseList

    def read_id(self, connection: sqlite3.Connection, expense_id: int):
        '''Read expense data by id'''
        cursor = connection.execute(f'SELECT * FROM {tableName} WHERE id = ?', (expense_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is not None:
            return ModelExpense(*row)
        return None

    def readWeeklyExpenseAmount(self, connection : sqlite3.Connection) -> float:
        try:
            # Dapatkan tanggal hari ini
            today = datetime.now()
            # Hitung awal dan akhir minggu
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)

            # Format tanggal ke dalam string

            # Query untuk mengambil total pengeluaran mingguan
            query = f"SELECT SUM(amount) FROM {tableName} WHERE time BETWEEN ? AND ?"
            cursor = connection.execute(query, (start_of_week.timestamp(), end_of_week.timestamp()))
            total_pengeluaran = cursor.fetchone()[0]
            cursor.close()

            # Jika total_pengeluaran adalah None, ubah menjadi 0
            return total_pengeluaran if total_pengeluaran is not None else 0
        except sqlite3.Error:
            return None

    def readDailyExpenseAmount(self, connection : sqlite3.Connection) -> float:
        try:
            # Dapatkan tanggal hari ini
            today = datetime.now().date()
            # Tentukan waktu awal dan akhir hari ini
            today_start = datetime.combine(today, datetime.min.time())
            today_end = datetime.combine(today, datetime.max.time())

            # Query untuk mengambil total pengeluaran pada hari ini
            query = f"SELECT SUM(amount) FROM {tableName} WHERE time BETWEEN ? AND ?"
            cursor = connection.execute(query, (today_start.timestamp(), today_end.timestamp()))
            total_pengeluaran = cursor.fetchone()[0]
            cursor.close()

            # Jika total_pengeluaran adalah None, ubah menjadi 0
            return total_pengeluaran if total_pengeluaran is not None else 0
        except sqlite3.Error:
            return None
   
    def readMonthlyExpenseAmount(self, connection: sqlite3.Connection) -> float:
        try:
            # Dapatkan tanggal bulan ini
            today = datetime.now()
            start_of_month = today.replace(day=1)
            end_of_month = start_of_month.replace(month=start_of_month.month % 12 + 1, day=1) - timedelta(days=1)

            # Query untuk mengambil total pengeluaran bulanan
            query = f"SELECT SUM(amount) FROM {tableName} WHERE time BETWEEN ? AND ?"
            cursor = connection.execute(query, (start_of_month.timestamp(), end_of_month.timestamp()))
            total_pengeluaran = cursor.fetchone()[0]
            cursor.close()

            # Jika total_pengeluaran adalah None, ubah menjadi 0
            return total_pengeluaran if total_pengeluaran is not None else 0
        except sqlite3.Error:
            return None

    def readYearlyExpenseAmount(self, connection: sqlite3.Connection) -> float:
        try:
            # Dapatkan tanggal tahun ini
            today = datetime.now()
            start_of_year = today.replace(month=1, day=1)
            end_of_year = today.replace(month=12, day=31)

            # Query untuk mengambil total pengeluaran tahunan
            query = f"SELECT SUM(amount) FROM {tableName} WHERE time BETWEEN ? AND ?"
            cursor = connection.execute(query, (start_of_year.timestamp(), end_of_year.timestamp()))
            total_pengeluaran = cursor.fetchone()[0]
            cursor.close()

            # Jika total_pengeluaran adalah None, ubah menjadi 0
            return total_pengeluaran if total_pengeluaran is not None else 0
        except sqlite3.Error:
            return None

    def insert(self, connection: sqlite3.Connection, data: ModelExpense):
        '''Insert expense data into the database'''
        try:
            columns = ', '.join(SQLExpense._insertColumnData)
            values = ', '.join(['?' for _ in range(SQLExpense._insertColumnLength)])
            query = f'INSERT INTO {tableName} ({columns}) VALUES ({values})'
            connection.execute(query, data.toListForInsert())
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