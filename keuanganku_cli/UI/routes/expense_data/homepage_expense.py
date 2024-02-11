from UI.utility.ui_print import kprint, kline, kprintCenter, kprintInfo
from UI.utility.clearscreen import clrscreen
from UI.user_input.input import getAny

from UI.routes.expense_data.detail_expense import UI_showExpenseDetail
from UI.routes.expense_data.insert_new_expense import UI_formNewExpense
from UI.routes.expense_data.routes.category import UI_homepageCategory
from UI.routes.expense_data.routes.graph import UI_weeklyDistributionGraph, UI_monthlyDistributionGraph, UI_yearlyDistributionGraph

from database.helper.sql_expense import SQLExpense, ModelExpense
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
        kprint("g : Graph\t")
        kline()
        userInput = str.lower(getAny(prompt='Command'))
        try:
            choosedIndex = int(userInput) -1
            if choosedIndex >= startIndex and choosedIndex < endIndex:
                exitStatus = UI_showExpenseDetail(data=expenseData[choosedIndex], conn=db.connection)
                if exitStatus:
                    DB_refreshExpenseData(db)
        except:
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
            elif userInput == "g":
                while True:
                    clrscreen()
                    kprint('Graph')
                    kline()
                    kprint('1. Weekly Distribution')
                    kprint('2. Monthly Distribution')
                    kprint('3. Yearly Distribution')
                    kprint('4. Back')
                    kline()
                    userInput = getAny('Command')
                    if userInput == '1':
                        UI_weeklyDistributionGraph(db)
                    elif userInput == '2':
                        UI_monthlyDistributionGraph(db)
                    elif userInput == '3':
                        UI_yearlyDistributionGraph(db)
                    elif userInput == '4':
                        break