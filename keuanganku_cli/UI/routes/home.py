from UI.utility.clearscreen import *
from UI.utility.ui_print import *
from UI.user_input.input import getInt

from error.invalid_input import *
from error.range_error import * 

from UI.error_handler.invalid_input import *
from database.db import KDatabase

from UI.routes.income_data.income_data import UI_income
from UI.routes.expense_data.homepage_expense import UI_expense

def ROUTE_income(db : KDatabase):
    UI_income(db)
def ROUTE_expense(db : KDatabase):
    UI_expense(db)
def ROUTE_advanceSummary(db : KDatabase):
    pass
def ROUTE_setting(db : KDatabase):
    pass
def ROUTE_exit(db : KDatabase):
    return 0

__routes__ = [
    ['Income Data',ROUTE_income],
    ['Expense Data',ROUTE_expense],
    ['Advance Summary',ROUTE_advanceSummary],
    ['Setting',ROUTE_setting],
    ['Exit', ROUTE_exit]
]
__routes_length__ = len(__routes__)

def UI_homepage(db : KDatabase):
    while True:
        clrscreen()
        kline()
        kprint("KeuanganKu-CLI 1.0")
        kline()
        for i in range(__routes_length__):
            kprint(f"{i + 1}. {__routes__[i][0]}")
        kline()
        try:
            userInput = getInt(f"Choose [1-{__routes_length__}] : ", range(1, __routes_length__ + 1))
            clrscreen()
            if __routes__[userInput-1][1](db) == 0:
                break
        except Exception as E:
            clrscreen()
            kprintInfo(E)
