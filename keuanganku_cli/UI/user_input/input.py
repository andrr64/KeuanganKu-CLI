from error.invalid_input import *

def getInt(prompt : str) -> any:
    try:
        return int(input(prompt))
    except:
        return KErrorInvalidInputType