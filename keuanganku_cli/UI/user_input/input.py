from error.invalid_input import *
from error.range_error import *

def getInt(prompt : str, expectedRange = None) -> int:
    try:
        userInput = int(input(prompt))
    except:
        raise KErrorInvalidInputType
    if expectedRange is not None and userInput not in expectedRange:
        raise KErrorRange(expectedRange)
    return userInput