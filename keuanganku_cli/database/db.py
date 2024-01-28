import sqlite3 as sql
import os
from database.helper import pemasukan, pengeluaran, kategori_pengeluaran, kategori_pemasukan

class KDatabase:
    __databaseFilename__ = "data.db"
    __databaseVersion__ = 1.0

    @staticmethod
    def isExist() -> bool:
        '''check is database file exist or not'''
        return os.path.isfile(KDatabase.__databaseFilename__)
    
    def __init__(self) -> None:
        self.connection = sql.Connection("data.db")

    def initMetadataTable(self):
        '''This function will create a table 'metadata' '''
        command = "CREATE TABLE IF NOT EXISTS metadata (VERSION REAL NOT NULL)"
        self.connection.execute(command)
        self.connection.execute(f"INSERT INTO metadata(VERSION) VALUES({self.__databaseVersion__})")

    def isConnected(self) -> bool:
        '''check is database connection OK or not'''
        return self.connection is not None

    def closeConnection(self):
        if self.isConnected:
            self.connection.close()

    def initDatabase(self):
        self.initMetadataTable()
        pemasukan.SQLPemasukan().initTable(self.connection)
        pengeluaran.SQLPengeluaran().initTable(self.connection)
        kategori_pemasukan.SQLKategoriPengeluaran().initTable(self.connection)
        kategori_pengeluaran.SQLKategoriPengeluaran().initTable(self.connection)
