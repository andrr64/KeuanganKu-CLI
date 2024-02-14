from database.model.model_expense_category import ModelExpenseCategory
from database.db import KDatabase
from database.helper.sql_expense_category import SQLExpenseCategory

from UI.utility.clearscreen import clrscreen
from UI.user_input.input import getAny
from UI.utility.ui_print import kprint, kprintInfo, kline

def DB_deleteExpenseCategory(db : KDatabase, data : ModelExpenseCategory) -> bool:
    clrscreen()
    if SQLExpenseCategory().b_delete(db.connection, data):
        kprintInfo('Operation success ^_^')
        return True
    kprintInfo('Something wrong...')
    return False

def UI_expenseCategoryDetail(db : KDatabase, data : ModelExpenseCategory) -> any:
    while True:
        clrscreen()
        kline()
        kprint("Detail")
        kline()
        kprint(f"Title\t: {data.title}")
        kline()
        kprint("Command")
        kprint("e: Back\t| d: Delete\t| u: Update")
        kline()
        userInput = str.lower(getAny('Command'))
        if userInput == 'd':
            clrscreen()
            userInput = str.lower(getAny('Are you sure? [Y/n]'))
            if userInput == 'y':
                DB_deleteExpenseCategory(db, data)
                return True
        elif userInput == 'e':
            return None