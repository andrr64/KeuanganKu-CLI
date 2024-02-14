from database.db import KDatabase
from database.helper.sql_expense_category import SQLExpenseCategory

from UI.routes.expense_data.routes.routes.insert_category import b_UI_insertCategory
from UI.utility.clearscreen import clrscreen
from UI.utility.ui_print import kprint, kline, kprintInfo
from UI.user_input.input import getAny

from UI.routes.expense_data.routes.routes.detail_category import UI_expenseCategoryDetail
global_ls_expenseCategory = []
global_ni_expenseCategoryLength = 0

def VAR_updateExpenseCategoryData(db : KDatabase):
    global global_ls_expenseCategory
    global global_ni_expenseCategoryLength
    global_ls_expenseCategory = SQLExpenseCategory().ls_readAll(db.connection)
    global_ni_expenseCategoryLength = len(global_ls_expenseCategory)

def b_ROUTE_insertCategory(db : KDatabase):
    try:
        return b_UI_insertCategory(db)
    except Exception as e:
        clrscreen()
        kprintInfo(e)
    return False

def UI_homepageCategory(db : KDatabase):
    global global_ls_expenseCategory
    global global_ni_expenseCategoryLength
    try:
        VAR_updateExpenseCategoryData(db)
        while True:
            clrscreen()
            kline()
            kprint("Expense Category")
            kline()
            kprint(f"{'No':<4} | Title")
            for ni_index, dyn_category in enumerate(global_ls_expenseCategory):
                kprint(f"{str(ni_index+1):<4} | {dyn_category}")
            kline()
            kprint("i : Insert\t") 
            kprint("e : Back\t| h : Help\t| r : Refresh") 
            kline()
            dyn_userInput = str.lower(getAny('Command'))
            try:
                ni_choosedIndex = int(dyn_userInput)-1
                if ni_choosedIndex >= 0 and ni_choosedIndex < global_ni_expenseCategoryLength:
                    if UI_expenseCategoryDetail(db, global_ls_expenseCategory[ni_choosedIndex]):
                        VAR_updateExpenseCategoryData(db)
            except:
                if dyn_userInput == 'e':
                    break
                elif dyn_userInput == 'i':
                    if b_ROUTE_insertCategory(db):
                        VAR_updateExpenseCategoryData(db)
    except Exception as e:
        clrscreen()
        kprintInfo(e)