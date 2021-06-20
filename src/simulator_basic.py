"""
Walt basic simulator
Python3 and SDL
# Only used in desktop python context

# Copyright (C) 2020 Angainor
"""

import sys
import time


sys.path.append("simulator")
from hardwareuiemulator import HardwareUIEmulator
sys.path.append("../modules")
from ui import UI
from displaymanager_basic import DisplayManager
from engineemulator import Engine


def event(touch):
    print("Touch", touch)


if __name__ == '__main__':
    print("start")
    engine = Engine()
    ui = UI(HardwareUIEmulator("basic1"))
    display_manager = DisplayManager(ui, engine)
    # result = display_manager.confirm_tx_screen("NYZO", "123.102000", "def4....a542", "")
    # print("Res", result)
    display_manager.run()
