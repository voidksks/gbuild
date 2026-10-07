RED = "\033[31m"
YELLOW = "\033[33m"
END = "\033[m"

def log_error(msg: str):
    print(f"{RED}[GBUILD]: {msg}{END}")

def log_warning(msg):
    print(f"{YELLOW}[GBUILD]: {msg}{END}")