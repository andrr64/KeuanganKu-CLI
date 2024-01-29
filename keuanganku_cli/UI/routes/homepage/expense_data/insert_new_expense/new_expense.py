from database.db import KDatabase
from UI.utility.ui_print import kprintInfo
from UI.utility.clearscreen import clrscreen

from UI.form.expense.expense_form import expenseForm

def ui_formNewExpense(db : KDatabase):
    while True:
        try:
            newData = expenseForm()
            if newData is None:
                break
            kprintInfo(newData)
        except Exception as e:
            clrscreen()
            kprintInfo(e)
