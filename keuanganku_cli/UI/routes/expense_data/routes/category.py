from database.db import KDatabase
from database.helper.sql_expense_category import SQLExpenseCategory

from UI.utility.clearscreen import clrscreen
from UI.utility.ui_print import kprint, kline, kprintInfo
from UI.user_input.input import getAny

def UI_homepageCategory(db : KDatabase):
    try:
        categoryList = SQLExpenseCategory().readAll(db.connection)

        while True:
            clrscreen()
            kline()
            kprint("Expense Category")
            kline()
            kprint(f"{'No':<4} | Title")
            for index, category in enumerate(categoryList):
                kprint(f"{str(index+1):<4} | {category}")
            kline()
            kprint("i : Insert\t") 
            kprint("e : Back\t| h : Help\t| r : Refresh") 
            kline()
            userInput = str.lower(getAny('Command'))
            if userInput == 'e':
                break
    except Exception as e:
        clrscreen()
        kprintInfo(e)