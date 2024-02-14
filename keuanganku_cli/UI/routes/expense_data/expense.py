from UI.utility.ui_print import kprint, kline, kprintCenter, kprintInfo
from UI.utility.clearscreen import clrscreen
from UI.user_input.input import getAny

from UI.routes.expense_data.detail_expense import UI_showExpenseDetail
from UI.routes.expense_data.insert_expense import UI_formNewExpense
from UI.routes.expense_data.routes.expense_category import UI_homepageCategory
from UI.routes.expense_data.routes.expense_graph import UI_weeklyDistributionGraph, UI_monthlyDistributionGraph, UI_yearlyDistributionGraph

from database.helper.sql_expense import SQLExpense, ModelExpense
from database.db import KDatabase

## Global Variable
global_ls_expenseData : list = []

global_fnc_printDataFunction  = None
global_ni_maxDataLength = 25

global_ni_pageNumber, global_ni_pageLength = 1,1
global_ni_startIndex, global_ni_endIndex = 0,0

global_nf_dailyExpenseAmount, global_nf_weeklyExpenseAmount = 0,0
global_nf_monthlyExpenseAmount, global_nf_yearlyExpenseAmount = 0,0

def UI_printExpenseData(listOfExpense, startNumber):
    ni_index = startNumber
    for dyn_data in listOfExpense:
        kprint(f'{ni_index} | {dyn_data}')
        ni_index += 1

def UI_printEmptyData():
    print()
    print()
    kprintCenter('Empty data', 50)
    print()
    print()

def UI_printWithData(
        ls_expenseData : list[ModelExpense],
        ni_startIndex : int,
        ni_endIndex : int,
        nf_dailyExpenseAmount : float,
        nf_weeklyExpenseAmount : float,
        nf_monthlyExpenseAmount : float,
        nf_yearlyExpenseAmount : float
):
        s_dailyExpensesAmount = f'{nf_dailyExpenseAmount:,.2f}'
        s_weeklyExpensesAmount = f'{nf_weeklyExpenseAmount:,.2f}'
        s_monthlyExpenseAmount = f'{nf_monthlyExpenseAmount:,.2f}'
        s_yearlyExpenseAmount = f'{nf_yearlyExpenseAmount:,.2f}'

        kprint("SUMMARY")
        kprint(f'Today\t\t: {s_dailyExpensesAmount:<20}Weekly\t: {s_weeklyExpensesAmount:<20}')
        kprint(f'Monthly\t: {s_monthlyExpenseAmount:<20}Yearly\t: {s_yearlyExpenseAmount:<20}')
        kline()
        kprint(f"No| {ModelExpense.printTableColumn()}")
        UI_printExpenseData(ls_expenseData[ni_startIndex:ni_endIndex], ni_startIndex + 1)

def VAR_refreshExpenseData(db : KDatabase):
    global global_ls_expenseData
    global global_fnc_printDataFunction, global_ni_pageNumber, global_ni_pageLength, global_ni_startIndex, global_ni_endIndex, global_ni_maxDataLength
    global global_nf_weeklyExpenseAmount, global_nf_dailyExpenseAmount, global_nf_monthlyExpenseAmount, global_nf_yearlyExpenseAmount
    
    global_ls_expenseData = SQLExpense().read_all(connection=db.connection)
    if global_ls_expenseData is None:
        ni_expenseDataLength = []
        global_fnc_printDataFunction = UI_printEmptyData
    else:
        def printWithData():
            UI_printWithData(
                global_ls_expenseData,
                global_ni_startIndex,
                global_ni_endIndex,
                global_nf_dailyExpenseAmount,
                global_nf_weeklyExpenseAmount,
                global_nf_monthlyExpenseAmount,
                global_nf_yearlyExpenseAmount
            )
        
        global_fnc_printDataFunction = printWithData
        ni_expenseDataLength = len(global_ls_expenseData)
        global_ni_maxDataLength = 25

        global_ni_pageNumber = 1
        global_ni_pageLength = global_ni_pageNumber if ni_expenseDataLength / global_ni_maxDataLength == 0 else int(ni_expenseDataLength/global_ni_maxDataLength) + 1

        global_ni_startIndex = 0
        global_ni_endIndex = global_ni_pageNumber * global_ni_maxDataLength

        if ni_expenseDataLength < global_ni_maxDataLength:
            global_ni_endIndex = ni_expenseDataLength
        
        global_nf_weeklyExpenseAmount     = SQLExpense().readWeeklyExpenseAmount(db.connection) 
        global_nf_dailyExpenseAmount      = SQLExpense().readDailyExpenseAmount(db.connection) 
        global_nf_monthlyExpenseAmount    = SQLExpense().readMonthlyExpenseAmount(db.connection)
        global_nf_yearlyExpenseAmount     = SQLExpense().readYearlyExpenseAmount(db.connection)

def UI_graph(db : KDatabase):
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

def UI_expense(db : KDatabase):
    VAR_refreshExpenseData(db)
    while True:
        clrscreen()
        kline()
        kprint("List of Expense")
        kline()
        global_fnc_printDataFunction()        
        kline()
        kprint('Command')
        kprint("i : Insert\t| s : Summary\t| c : Category") 
        kprint("e : Back\t| h : Help\t| r : Refresh") 
        kprint("s : Sort by") 
        kprint("g : Graph\t| f : Filter\t| fc: Fast Command")
        kline()
        dyn_userInput = str.lower(getAny(prompt='Command'))
        try:
            ni_choosedIndex = int(dyn_userInput) -1
            if ni_choosedIndex >= global_ni_startIndex and ni_choosedIndex < global_ni_endIndex:
                exitStatus = UI_showExpenseDetail(data=global_ls_expenseData[ni_choosedIndex], conn=db.connection)
                if exitStatus:
                    VAR_refreshExpenseData(db)
        except:
            if dyn_userInput == "e":
                return 
            elif dyn_userInput == "i":
                b_dataCreated = UI_formNewExpense(db)
                if b_dataCreated:
                    VAR_refreshExpenseData(db)
            elif dyn_userInput == "r":
                VAR_refreshExpenseData(db)
            elif dyn_userInput == "c":
                UI_homepageCategory(db)
            elif dyn_userInput == "g":
                UI_graph(db)