from UI.routes.homepage.home import *
from database.db import KDatabase

if __name__ == "__main__":

    # Check is database exist or not
    if not KDatabase.isExist():
        KDatabase().initDatabase()

    db = KDatabase()
    ui_homepage(db)
    if KDatabase.isExist():
        db.closeConnection()