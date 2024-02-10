from database.db import KDatabase
from UI.utility.ui_print import kprintInfo
from UI.utility.clearscreen import clrscreen

from UI.form.expense.new_expense import expenseForm
from database.helper.expense import SQLExpense

def UI_formNewExpense(db : KDatabase):
    while True:
        try:
            newData = expenseForm(db=db)
            if newData is None:
                break  
            else:
                clrscreen()
                if SQLExpense().insert(db.connection, newData):
                    kprintInfo("Success ^_^")
                    return True
                else:
                    kprintInfo("Something wrong")
                    return False
        except Exception as e:
            clrscreen()
            kprintInfo(e)
            return False