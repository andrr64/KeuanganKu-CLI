from UI.utility.clearscreen import clrscreen
from UI.utility.ui_print import kprint, kline, kprintInfo
from UI.user_input.input import getAny

from database.db import KDatabase

from database.helper.sql_expense_category import SQLExpenseCategory, ModelExpenseCategory

__ni_maxTitleChar = 30

def __b_CHECK_isNameLengthOk(title : str):
    return len(title) < __ni_maxTitleChar

def b_UI_insertCategory(db : KDatabase):
    s_newExpenseCategoryTitle = ''
    while True:
        clrscreen()        
        kline()
        kprint("New Expense Category")
        kprint(f"Type '$' to exit")
        kline()
        s_newExpenseCategoryTitle = getAny('Category Title')
        
        clrscreen()
        if s_newExpenseCategoryTitle == '$':
            return False
        elif not __b_CHECK_isNameLengthOk(s_newExpenseCategoryTitle):
            kprintInfo(f"Max char length is {__ni_maxTitleChar} ok. insert again")
            continue
        dyn_newExpenseCategoryData = ModelExpenseCategory(title=s_newExpenseCategoryTitle)
        b_isDataCreated = SQLExpenseCategory().b_insert(db=db.connection, data=dyn_newExpenseCategoryData)
        if b_isDataCreated:
            kprintInfo('Success ^_^')
            return True
        else:
            kprintInfo('Something wrong...')
            return False