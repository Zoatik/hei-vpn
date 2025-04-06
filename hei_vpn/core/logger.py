class ANSI:
    CTRL = "\x1b["
    RESET = 0
    BOLD = 1
    ITALIC = 3
    UNDERLINE = 4
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37

class Logger:
    def __init__(self, tag="", styles=None):
        self.tag = tag
        self.styles = styles or []

    def log(self, msg):
        style = ANSI.CTRL + ";".join(map(str, self.styles)) + "m"
        reset = ANSI.CTRL + str(ANSI.RESET) + "m"
        tag = f"[{self.tag}] " if self.tag else ""
        print(style + tag + msg + reset)

infoLogger = Logger("INFO", [ANSI.BLUE+60])
warningLogger = Logger("WARNING", [ANSI.YELLOW])
errorLogger = Logger("ERROR", [ANSI.BOLD, ANSI.RED])
vpnLogger = Logger("", [ANSI.ITALIC, ANSI.BLACK+60])