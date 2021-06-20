
from hardwareuibasic import HardwareUI
from ui import UI
from displaymanager_basic import DisplayManager
from enginebasic import Engine
from dev_basic import dev_message
from machine import Pin
from time import sleep_ms


def start():
    print("LOG: Start")
    test = Pin(35, Pin.IN, Pin.PULL_UP)
    sleep_ms(50)
    if test.value() == 0:
        print("LOG: Entering Dev mode")
        # Set dev mode, don't start engine
        dev_message()
    else:
        print("LOG: Entering standalone mode")
        engine = Engine()
        ui = UI(HardwareUI(orientation=1))
        display_manager = DisplayManager(ui, engine)
        display_manager.run()


if __name__ == '__main__':
    start()
