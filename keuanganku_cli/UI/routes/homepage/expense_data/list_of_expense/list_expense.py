import sqlite3 

from UI.utility.ui_print import kprintInfo, kprint, kline, kprintCenter
from UI.utility.clearscreen import clrscreen

from UI.user_input.input import getAny

from database.helper.expense import SQLExpense

def printExpenseList(listOfExpense, startNumber):
    i = startNumber
    for data in listOfExpense:
        print(f' {i} | {data}')
        i += 1

def ui_listOfExpense(connection : sqlite3.Connection):
    listOfExpense : list = SQLExpense().read_all(connection=connection)
    if listOfExpense is None:
        clrscreen()
        kprintInfo("Empty data :(")
        return
    
    dataLength = len(listOfExpense)

    maxDataLength = 25

    pageNumber = 1
    pageLength = pageNumber if dataLength / maxDataLength == 0 else int(dataLength/maxDataLength) + 1

    startIndex = 0
    endIndex = pageNumber * maxDataLength

    if dataLength < maxDataLength:
        endIndex = dataLength
    
    weeklyExpensesAmount = SQLExpense().readTotalPengeluaranMingguan(connection) 
    dailyExpensesAmount = SQLExpense().readTotalPengeluaranHarian(connection) 

    dailyExpensesAmountStr = f'{dailyExpensesAmount:,.0f}'
    weeklyExpensesAmountStr = f'{weeklyExpensesAmount:<30,.0f}'

    while True:
        clrscreen()
        kline()
        kprint("List of Expense")
        kline()
        kprint("SUMMARY")
        kprint(f'Daily\t: {dailyExpensesAmountStr:<20}Weekly\t: {weeklyExpensesAmountStr:<20}')
        kline()
        print()
        printExpenseList(listOfExpense[startIndex:endIndex], startIndex + 1)
        print()
        kline()
        kprintCenter("e : Back\t| h : help", 50) 
        kprintCenter(f'{pageNumber} of {pageLength}', 50)
        kline()
        userInput = getAny(prompt='Choose')
        try:
            choosedIndex = int(userInput) -1
            if choosedIndex >= startIndex and choosedIndex < endIndex:
                kprintInfo(listOfExpense[choosedIndex])
        except:
            if str.lower(userInput) == "e":
                return 
                