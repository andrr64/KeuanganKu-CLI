from UI.utility.clearscreen import *
from UI.utility.ui_print import *
from UI.user_input.input import getInt
from error.invalid_input import *
from UI.error_handler.invalid_input import *

def routeIncomeData():
    clrscreen()
def routeExpenseData():
    pass
def routeAdvanceSummary():
    pass
def routeSetting():
    pass
def routeExit():
    return 0

__routes__ = [
    ['Income Data',routeIncomeData],
    ['Expense Data',routeExpenseData],
    ['Advance Summary',routeAdvanceSummary],
    ['Setting',routeSetting],
    ['Exit', routeExit]
]
__routes_length__ = len(__routes__)

def ui_homepage():
    while True:
        clrscreen()
        kline()
        kprint("KeuanganKu-CLI 1.0")
        kline()
        for i in range(__routes_length__):
            kprint(f"{i + 1}. {__routes__[i][0]}")
        kline()
        userInput = getInt(f"Choose [1-{__routes_length__}] : ")
        if isinstance(userInput, KErrorInvalidInputType):
            errorHandlerInvalidInputType()
        else:
            if __routes__[userInput -1][1]() == 0:
                clrscreen()
                break