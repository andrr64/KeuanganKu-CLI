from database.model.expense import ModelExpense

from error.invalid_input import KErrorInvalidInputType
from error.range_error import KErrorRange

from datetime import datetime

from database.db import KDatabase
from database.helper.expense_category import SQLExpenseCategory
from database.model.expense_category import ModelExpenseCategory

from UI.utility.clearscreen import clrscreen
from UI.utility.ui_print import kprintInfo, kline
from UI.user_input.input import getInt

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
    clrscreen()
    print('+--------------------------+')
    print("Expense Time")
    print('+--------------------------+')
    print("time format is dd/mm/yyyy hh:mm (use 24hr)")
    print("type 'now' if time is now -> now")
    print("type 'now_dt' if date is now -> now_dt 12:00")
    print('+--------------------------+')
    userInput = input("Time       : ")
    if userInput.lower() == 'now':
        return datetime.now()
    elif userInput.lower().startswith('now_dt'):
        _, time_str = userInput.split(' ')
        current_date = datetime.now().strftime("%d/%m/%Y")
        datetime_format = "%d/%m/%Y %H:%M"
        return datetime.strptime(f"{current_date} {time_str}", datetime_format)
    else:
        datetime_format = "%d/%m/%Y %H:%M"
        try:
            userInput = datetime.strptime(userInput, datetime_format)
            return userInput
        except ValueError as E:
            raise E
def fieldCategory(db: KDatabase) -> ModelExpenseCategory:
    listCategory = SQLExpenseCategory().read_all(db=db.connection)
    if listCategory is None:
        # todo: Handle when listCategory is empty
        pass
    while True:
        try:
            clrscreen()
            kline()
            print("Expense Category")
            kline()
            for i, category in enumerate(listCategory):
                category : ModelExpenseCategory = category
                print(f"{i+1}. {category.title}")
            kline()
            userInput = getInt("Choose : ", expectedRange=range(1, len(listCategory) + 1))
            return listCategory[userInput-1]
        except Exception as E:
            clrscreen()
            kprintInfo(E)

def expenseForm(db : KDatabase):
    expenseTitle = ""
    expenseAmount = ""
    expenseRate = 10
    expenseCategory = 1
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
            expenseCategory : ModelExpenseCategory = fieldCategory(db=db)
            if expenseCategory is None:
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
            category_id= expenseCategory.id, 
            rate= expenseRate
        )
