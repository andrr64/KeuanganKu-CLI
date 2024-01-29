from database.model.expense import ModelExpense

from error.invalid_input import KErrorInvalidInputType
from error.range_error import KErrorRange

from datetime import datetime
from UI.utility.clearscreen import clrscreen
from UI.utility.ui_print import kprintInfo

def fieldTitle():
    userInput = input('Title      : ')
    if userInput == '$':
        return None
    elif len(userInput) == 0:
        raise Exception("Title can't empty")
    return userInput
def fieldAmount():
    inputAmount = input("Amount     : ")
    if inputAmount == '$':
        return None
    try:
        inputAmount = float(inputAmount)
        if inputAmount <= 0:
            raise KErrorRange
        return inputAmount
    except:
        raise KErrorInvalidInputType
def fieldTime():
    print('+--------------------------+')
    print("time format is dd/mm/yyyy hh:mm (use 24hr)")
    print("type 'now' if time is now")
    print('+--------------------------+')
    userInput = input("Time       : ")
    if userInput.lower() == 'now':
        return datetime.now()
    else:
        datetime_format = "%d/%m/%Y %H:%M"
        try:
            userInput = datetime.strptime(userInput, datetime_format)
            return userInput
        except ValueError as E:
            raise E

def expenseForm():
    expenseTitle = ""
    expenseAmount = ""
    expenseRate = 10
    expenseCategoryId = 1
    expenseTime = None
    while True:
        try:
            clrscreen()
            print('+--------------------------+')
            print("Expense Form")
            print("Type '$' to exit")
            print('+--------------------------+')
            expenseTitle = fieldTitle()
            if expenseTitle is None:
                return None
            expenseAmount = fieldAmount()
            if expenseAmount is None:
                return None
            expenseTime = fieldTime()
            if expenseTime is None:
                return None
        except Exception as E:
            clrscreen()
            kprintInfo(E)
            continue
        
        return ModelExpense(
            id=-1, 
            title=expenseTitle, 
            time=expenseTime, 
            amount= expenseAmount, 
            category_id= expenseCategoryId, 
            rate= expenseRate
        )
