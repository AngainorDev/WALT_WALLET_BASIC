
from hardwareuibasic import HardwareUI
from ui import UI
from displaymanager_basic import DisplayManager
from enginebasic import Engine


def start():
    print("LOG: Start")
    engine = Engine()
    ui = UI(HardwareUI())
    display_manager = DisplayManager(ui, engine)
    # result = display_manager.confirm_tx("NYZO", "123.102000", "def4....a542", "")
    # print("Res", result)
    display_manager.run()


if __name__ == '__main__':
    start()
