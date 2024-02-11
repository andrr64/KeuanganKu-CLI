from UI.routes.home import UI_homepage
from database.db import KDatabase
from UI.utility.ui_print import kprintInfo
from UI.utility.clearscreen import clrscreen

def __raise_module_error(module_name):
    raise Exception(f"{module_name} not found, install it using 'pip install {module_name}'")

def __CHECK_modules():
    try:
        import matplotlib
        del matplotlib
    except:
        __raise_module_error('matplotlib')
    try:
        import numpy as np
        del np
    except:
        __raise_module_error('numpy') 
    
def __CHECK_database():
    try:
        if not KDatabase.isExist():
            KDatabase().initDatabase()
    except:
        errorMsg = "Database error, something wrong..."
        raise Exception(errorMsg)
    
def CHECK_isEverythingOkay():
    try:
        __CHECK_database()
        __CHECK_modules()
        return True
    except Exception as e:
        kprintInfo(e)
        return False
    
if __name__ == "__main__":
    if CHECK_isEverythingOkay() is True:
        db = KDatabase()
        UI_homepage(db)
        if KDatabase.isExist():
            db.closeConnection()