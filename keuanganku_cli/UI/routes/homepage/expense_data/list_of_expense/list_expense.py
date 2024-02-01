import sqlite3 

from UI.utility.ui_print import kprintInfo, kprint, kline
from UI.utility.clearscreen import clrscreen

from database.helper.expense import SQLExpense

def ui_listOfExpense(connection : sqlite3.Connection):
    listOfExpense = SQLExpense().read_all(connection=connection)
    while True:
        clrscreen()
        kline()
        kprint("List of Expense")
        kline()
        for i, expense in enumerate(listOfExpense):
            print(f" {i + 1} | {expense} |")
        kline()
        input()
        