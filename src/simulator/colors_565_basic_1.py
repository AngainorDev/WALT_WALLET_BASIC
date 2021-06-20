
if 'const' not in globals():
    print("Emulating const")
    def const(fn):
        return fn

_RED = const(0xF800)
_BLACK = const(0x0000)
_BLUE = const(0x001F)
_GREEN = const(0x07E0)
_CYAN = const(0x07FF)
_MAGENTA = const(0xF81F)
_YELLOW = const(0xFFE0)
_WHITE = const(0xFFFF)
_DARK_GRAY = const(0x39E7)
_LIGHT_GRAY = const(0x9CF3)

# Color Theme
BG = const(0)
TEXT = const(0xFFFF)
TEXT2 = const(0xCE59)
WALT = const(0x7000)  # nyzo color for walt boot logo
NYZO = const(0x7000)  # nyzo color
YES = const(0x07E0)
NO = const(0xF800)
STATUS_BG = const(0x39E7)
SELECTED = const(0x9CF3)
ICON = const(0x7000)

A0 = const(0x39E7)
A1 = const(0x9CF3)
A2 = const(0x7000)