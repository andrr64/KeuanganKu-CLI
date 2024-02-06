def kline(n = 50):
    print(f"+{'-' * n}+")

def kprint(text : str):
    print(f" {text}")

def kprintCenter(text : str, length : int):
    print(text.center(length))

def kprintInfo(msg : str):
    print(f"{msg}")
    input(f"press any to continue... ")