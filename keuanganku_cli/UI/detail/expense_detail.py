from UI.utility.clearscreen import clrscreen
from UI.utility.ui_print import kline, kprint, kprintCenter
from UI.user_input.input import getAny

from database.model.expense import ModelExpense

import sqlite3 as sql

def showExpenseDetail(data : ModelExpense, conn : sql.Connection):
    while True:
        clrscreen()
        kprint("Expense Detail")
        kline()
        kprint(f"Title\t\t: {data.title}")
        kprint(f"Amount\t\t: {data.amount:,.0f}")
        kprint(f"Date\t\t: {data.timeToStringFormat}")
        kprint(f"Category\t: {data.category.title}")
        kline()
        kprintCenter("e : back | d : Delete | c : change", 50)  
        kline()
        userInput = getAny("Command")        
        if str.lower(userInput) == "e":
            break