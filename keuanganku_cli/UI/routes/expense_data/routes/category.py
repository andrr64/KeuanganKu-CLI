from database.db import KDatabase
from database.helper.sql_expense_category import SQLExpenseCategory

from UI.utility.clearscreen import clrscreen
from UI.utility.ui_print import kprint, kline, kprintInfo
from UI.user_input.input import getAny

from UI.routes.expense_data.routes.routes.detail_category import UI_expenseCategoryDetail
global_categoryList = []
global_categoryListLen = 0

def VAR_updateExpenseCategoryList(db : KDatabase):
    global global_categoryList
    global global_categoryListLen
    global_categoryList = SQLExpenseCategory().readAll(db.connection)
    global_categoryListLen = len(global_categoryList)

def UI_homepageCategory(db : KDatabase):
    global global_categoryList
    global global_categoryListLen
    try:
        VAR_updateExpenseCategoryList(db)
        while True:
            clrscreen()
            kline()
            kprint("Expense Category")
            kline()
            kprint(f"{'No':<4} | Title")
            for index, category in enumerate(global_categoryList):
                kprint(f"{str(index+1):<4} | {category}")
            kline()
            kprint("i : Insert\t") 
            kprint("e : Back\t| h : Help\t| r : Refresh") 
            kline()
            userInput = str.lower(getAny('Command'))
            try:
                choosedIndex = int(userInput)-1
                if choosedIndex >= 0 and choosedIndex < global_categoryListLen:
                    if UI_expenseCategoryDetail(db, global_categoryList[choosedIndex]):
                        VAR_updateExpenseCategoryList(db)
            except:
                if userInput == 'e':
                    break
    except Exception as e:
        clrscreen()
        kprintInfo(e)