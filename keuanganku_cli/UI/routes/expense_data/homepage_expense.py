from UI.utility.ui_print import kprint, kline, kprintCenter
from UI.utility.clearscreen import clrscreen
from UI.user_input.input import getAny

from UI.routes.expense_data.detail_expense import showExpenseDetail
from UI.routes.expense_data.insert_new_expense import UI_formNewExpense
from UI.routes.expense_data.routes.category import UI_homepageCategory

from database.helper.sql_expense import SQLExpense
from database.model.model_expense import ModelExpense
from database.db import KDatabase

## Global Variable
expenseData : list = []

printDataFunction  = None
maxDataLength = 25

pageNumber, pageLength = 1,1
startIndex, endIndex = 0,0

dailyExpenseAmount, weeklyExpenseAmount = 0,0
monthlyExpenseAmount, yearlyExpenseAmount = 0,0

def UI_printExpenseData(listOfExpense, startNumber):
    i = startNumber
    for data in listOfExpense:
        kprint(f'{i} | {data}')
        i += 1

def UI_printEmptyData():
    print()
    print()
    kprintCenter('Empty data', 50)
    print()
    print()

def UI_printWithData(
        expenseData : list[ModelExpense],
        startIndex : int,
        endIndex : int,
        dailyExpenseAmount : float,
        weeklyExpenseAmount : float,
        monthlyExpenseAmount : float,
        yearlyExpenseAmount : float
):
        dailyExpensesAmountStr = f'{dailyExpenseAmount:,.2f}'
        weeklyExpensesAmountStr = f'{weeklyExpenseAmount:,.2f}'
        monthlyExpenseAmountStr = f'{monthlyExpenseAmount:,.2f}'
        yearlyExpenseAmountStr = f'{yearlyExpenseAmount:,.2f}'

        kprint("SUMMARY")
        kprint(f'Today\t\t: {dailyExpensesAmountStr:<20}Weekly\t: {weeklyExpensesAmountStr:<20}')
        kprint(f'Monthly\t: {monthlyExpenseAmountStr:<20}Yearly\t: {yearlyExpenseAmountStr:<20}')
        kline()
        kprint(f"No| {ModelExpense.printTableColumn()}")
        UI_printExpenseData(expenseData[startIndex:endIndex], startIndex + 1)

def DB_refreshExpenseData(db : KDatabase):
    global expenseData
    global printDataFunction, pageNumber, pageLength, startIndex, endIndex, maxDataLength
    global weeklyExpenseAmount, dailyExpenseAmount, monthlyExpenseAmount, yearlyExpenseAmount
    
    expenseData = SQLExpense().read_all(connection=db.connection)
    if expenseData is None:
        expenseDataLength = []
        printDataFunction = UI_printEmptyData
    else:
        def printWithData():
            UI_printWithData(
                expenseData,
                startIndex,
                endIndex,
                dailyExpenseAmount,
                weeklyExpenseAmount,
                monthlyExpenseAmount,
                yearlyExpenseAmount
            )
        
        printDataFunction = printWithData
        expenseDataLength = len(expenseData)
        maxDataLength = 25

        pageNumber = 1
        pageLength = pageNumber if expenseDataLength / maxDataLength == 0 else int(expenseDataLength/maxDataLength) + 1

        startIndex = 0
        endIndex = pageNumber * maxDataLength

        if expenseDataLength < maxDataLength:
            endIndex = expenseDataLength
        
        weeklyExpenseAmount     = SQLExpense().readWeeklyExpenseAmount(db.connection) 
        dailyExpenseAmount      = SQLExpense().readDailyExpenseAmount(db.connection) 
        monthlyExpenseAmount    = SQLExpense().readMonthlyExpenseAmount(db.connection)
        yearlyExpenseAmount     = SQLExpense().readYearlyExpenseAmount(db.connection)

def UI_expense(db : KDatabase):
    DB_refreshExpenseData(db)
    while True:
        clrscreen()
        kline()
        kprint("List of Expense")
        kline()
        printDataFunction()        
        kline()
        kprint("i : Insert\t| s : Summary\t| c : Category") 
        kprint("e : Back\t| h : Help\t| r : Refresh") 
        kline()
        userInput = getAny(prompt='Command')
        try:
            choosedIndex = int(userInput) -1
            if choosedIndex >= startIndex and choosedIndex < endIndex:
                showExpenseDetail(data=expenseData[choosedIndex], conn=db.connection)
        except:
            userInput = str.lower(userInput)
            if userInput == "e":
                return 
            elif userInput == "i":
                dataCreated = UI_formNewExpense(db)
                if dataCreated:
                    DB_refreshExpenseData(db)
            elif userInput == "r":
                pass
            elif userInput == "c":
                UI_homepageCategory(db)
                