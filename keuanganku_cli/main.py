from UI.routes.home import UI_homepage
from database.db import KDatabase

def __CHECK_matplotlibModule():
    try:
        import matplotlib
        del matplotlib
    except:
        errorMsg = 'Matplotlib is not found, install it using pip command "pip install matplotlib"'
        raise Exception(errorMsg)
    
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
        __CHECK_matplotlibModule()
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