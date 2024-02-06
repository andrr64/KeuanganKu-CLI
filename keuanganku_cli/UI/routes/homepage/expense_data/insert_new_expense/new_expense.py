from database.db import KDatabase
from UI.utility.ui_print import kprintInfo
from UI.utility.clearscreen import clrscreen

from keuanganku_cli.UI.form.expense.new_expense import expenseForm
from database.helper.expense import SQLExpense

def ui_formNewExpense(db : KDatabase):
    while True:
        try:
            newData = expenseForm(db=db)
            if newData is None:
                break  
            else:
                clrscreen()
                if SQLExpense().insert(db.connection, newData):
                    kprintInfo("Success ^_^")
                else:
                    kprintInfo("Something wrong")
                break
        except Exception as e:
            clrscreen()
            kprintInfo(e)