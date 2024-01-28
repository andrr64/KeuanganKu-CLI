from UI.utility.ui_print import kline, kprint, kprintInfo
from UI.utility.clearscreen import clrscreen
from database.db import *

from UI.user_input.input import getInt

def routeBack(db : KDatabase):
    return 0
def routeInsertNewData(db : KDatabase):
    pass
def routeInsertNewCategory(db : KDatabase):
    pass
def routeListOfExpense(db : KDatabase):
    pass

__routes__ = [
    ["List of Expense", ],
    ["Insert New Expense",],
    ["Insert New Expense Category", ],
    ["Back", routeBack]
]
__routelength__ = len(__routes__)

def ui_incomeData(db : KDatabase):
    while True:
        clrscreen()
        kline()
        kprint("Income Data")
        kline()
        for i in range(__routelength__):
            kprint(f"{i + 1}. {__routes__[i][0]}")
        kline()
        userInput = getInt("Choose : ", expectedRange=range(1, __routelength__ + 1))

        if __routes__[userInput-1][1](db) == 0:
            break
