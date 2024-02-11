from database.db import KDatabase
from UI.utility.ui_print import kprintInfo
from UI.utility.clearscreen import clrscreen

def __CHECK_modules():
    try:
        import matplotlib
        del matplotlib
        import numpy as np
        del np
        import tzlocal
        del tzlocal
    except:
        raise Exception(f"All required module not installed\nRead 'readme.txt'")
    
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
    clrscreen()
    if CHECK_isEverythingOkay() is True:
        from UI.routes.home import UI_homepage

        db = KDatabase()
        UI_homepage(db)
        if KDatabase.isExist():
            db.closeConnection()