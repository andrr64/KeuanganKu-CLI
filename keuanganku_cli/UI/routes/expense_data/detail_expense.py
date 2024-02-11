from UI.utility.clearscreen import clrscreen
from UI.utility.ui_print import kline, kprint, kprintCenter, kprintInfo
from UI.user_input.input import getAny

from database.helper.sql_expense import SQLExpense, ModelExpense

import sqlite3 as sql


def UI_showExpenseDetail(data : ModelExpense, conn : sql.Connection):
    while True:
        clrscreen()
        kline()
        kprint("Expense Detail")
        kline()
        kprint(f"Title\t\t: {data.title}")
        kprint(f"Amount\t\t: {data.amount:,.0f}")
        kprint(f"Date\t\t: {data.timeToStringFormat}")
        kprint(f"Category\t: {data.category.title}")
        kline()
        kprintCenter("e : back | d : Delete | c : change", 50)  
        kline()
        userInput = str.lower(getAny('Command'))        
        if userInput == "e":
            return False
        elif userInput == "d":
            clrscreen()
            if str.lower(getAny('Are you sure? [Y/n]')) == 'y':
                clrscreen()
                if SQLExpense().delete(conn, data):
                    kprintInfo('Success ^_^')
                else:
                    kprintInfo('Failed :(, something wrong')
            return True