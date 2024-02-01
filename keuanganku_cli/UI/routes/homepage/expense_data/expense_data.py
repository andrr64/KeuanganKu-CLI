from UI.utility.ui_print import kline, kprint
from UI.utility.clearscreen import clrscreen

from UI.routes.homepage.expense_data.insert_new_expense.new_expense import ui_formNewExpense
from UI.routes.homepage.expense_data.list_of_expense.list_expense import ui_listOfExpense

from database.db import *

from UI.user_input.input import getInt

def routeBack(db : KDatabase):
    return 0
def routeInsertNewData(db : KDatabase):
    ui_formNewExpense(db)
def routeInsertNewCategory(db : KDatabase):
    pass
def routeListOfExpense(db : KDatabase):
    ui_listOfExpense(connection=db.connection)

__routes__ = [
    ["List of Expense", routeListOfExpense],
    ["Insert New Expense", routeInsertNewData],
    ["Insert New Expense Category", routeInsertNewCategory],
    ["Back", routeBack]
]
__routelength__ = len(__routes__)

def ui_expenseData(db : KDatabase):
    while True:
        clrscreen()
        kline()
        kprint("Expense Data")
        kline()
        for i in range(__routelength__):
            kprint(f"{i + 1}. {__routes__[i][0]}")
        kline()
        userInput = getInt("Choose : ", expectedRange=range(1, __routelength__ + 1))
        if __routes__[userInput-1][1](db) == 0:
            break
