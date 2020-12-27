import colorama
colorama.init()

BLUE = u'\033[94m'
GREEN = u'\033[92m'
YELLOW = u'\033[93m'
RED = u'\033[91m'
WHITE = u''
END = u'\033[0m'


def message(text, color, end="\n"):
    colors = {"blue": BLUE, "green": GREEN, "yellow": YELLOW, "red": RED, "white": WHITE}
    print(f'{colors[color]}>>> {END}{text}', end=end)
