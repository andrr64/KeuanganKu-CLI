import sqlite3 

from UI.utility.ui_print import kprintInfo, kprint, kline, kprintCenter
from UI.utility.clearscreen import clrscreen

from UI.user_input.input import getAny

from keuanganku_cli.UI.routes.homepage.expense_data.detail_expense import showExpenseDetail

from keuanganku_cli.UI.routes.homepage.expense_data.insert_new_expense import UI_formNewExpense

from database.helper.expense import SQLExpense
from database.model.expense import ModelExpense

from database.db import KDatabase

def printExpenseList(listOfExpense, startNumber):
    i = startNumber
    for data in listOfExpense:
        print(f' {i} | {data}')
        i += 1

def DB_getExpenseData(db : KDatabase):
    return {
        'data' : SQLExpense().read_all(connection=db.connection),
    }

def UI_expense(db : KDatabase):
    expenseData : list = SQLExpense().read_all(connection=db.connection)
    if expenseData is None:
        clrscreen()
        kprintInfo("Empty data :(")
        return
    
    expenseDataLength = len(expenseData)

    maxDataLength = 25

    pageNumber = 1
    pageLength = pageNumber if expenseDataLength / maxDataLength == 0 else int(expenseDataLength/maxDataLength) + 1

    startIndex = 0
    endIndex = pageNumber * maxDataLength

    if expenseDataLength < maxDataLength:
        endIndex = expenseDataLength
    
    weeklyExpensesAmount = SQLExpense().readTotalPengeluaranMingguan(db.connection) 
    dailyExpensesAmount = SQLExpense().readTotalPengeluaranHarian(db.connection) 

    dailyExpensesAmountStr = f'{dailyExpensesAmount:,.0f}'
    weeklyExpensesAmountStr = f'{weeklyExpensesAmount:,.0f}'

    while True:
        clrscreen()
        kline()
        kprint("List of Expense")
        kline()
        kprint("SUMMARY")
        kprint(f'Today\t: {dailyExpensesAmountStr:<20}Weekly\t: {weeklyExpensesAmountStr:<20}')
        kline()
        kprint(f"No| {ModelExpense.printTableColumn()}")
        printExpenseList(expenseData[startIndex:endIndex], startIndex + 1)
        kprintCenter(f'{pageNumber} of {pageLength}', 50)
        kline()
        kprint("i : Insert\t| a : Advance Summary") 
        kprint("e : Back\t| h : help") 
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
                UI_formNewExpense(db)
                