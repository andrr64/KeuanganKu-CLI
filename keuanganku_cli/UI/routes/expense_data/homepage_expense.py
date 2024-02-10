from UI.utility.ui_print import kprint, kline, kprintCenter
from UI.utility.clearscreen import clrscreen
from UI.user_input.input import getAny
from UI.routes.expense_data.detail_expense import showExpenseDetail
from UI.routes.expense_data.insert_new_expense import UI_formNewExpense

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

def UI_printExpenseData(listOfExpense, startNumber):
    i = startNumber
    for data in listOfExpense:
        print(f' {i} | {data}')
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
        weeklyExpenseAmount : float
):
        dailyExpensesAmountStr = f'{dailyExpenseAmount:,.0f}'
        weeklyExpensesAmountStr = f'{weeklyExpenseAmount:,.0f}'

        kprint("SUMMARY")
        kprint(f'Today\t: {dailyExpensesAmountStr:<20}Weekly\t: {weeklyExpensesAmountStr:<20}')
        kline()
        kprint(f"No| {ModelExpense.printTableColumn()}")
        UI_printExpenseData(expenseData[startIndex:endIndex], startIndex + 1)

def DB_refreshExpenseData(db : KDatabase):
    global expenseData
    global printDataFunction, pageNumber, pageLength, startIndex, endIndex, maxDataLength
    global weeklyExpenseAmount, dailyExpenseAmount
    
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
                weeklyExpenseAmount
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
        
        weeklyExpenseAmount = SQLExpense().readTotalPengeluaranMingguan(db.connection) 
        dailyExpenseAmount = SQLExpense().readTotalPengeluaranHarian(db.connection) 

def UI_expense(db : KDatabase):
    DB_refreshExpenseData(db)
    while True:
        clrscreen()
        kline()
        kprint("List of Expense")
        kline()
        printDataFunction()        
        kline()
        kprint("i : Insert\t| a : Advance Summary") 
        kprint("e : Back\t| h : help | r : Refresh") 
        kline()
        userInput = getAny(prompt='Choose')
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
                