from machine import Pin, PWM
from ble_temperature import BLETemperature
import gc
import urandom
from sys import stdin
from select import select
from os import statvfs
from baseengine import BaseEngine


__version__ = "0.3c"


class CoreEngine:
    def __init__(self):
        self.BLE = False
        self.ble_object = None
        self.WIFI = False
        self.contrasts = [100, 250, 512, 750, 1023]
        self.contrast_index = 2
        #self.backlight = PWM(Pin(4, Pin.OUT), 5000)
        self.backlight = PWM(Pin(4, Pin.OUT))
        # workaround soft reset
        self.backlight.deinit()
        self.backlight.init(freq=5000, duty=self.contrasts[self.contrast_index])
        self.backlight.duty(self.contrasts[self.contrast_index])
        self.i = 0

    def toggle_ble(self):
        self.BLE = not self.BLE
        print("LOG: Toggle BLE Simu", self.BLE)
        self.i = 0
        if self.BLE:
            # create if needed
            if self.ble_object is None:
                self.ble_object = BLETemperature(active=True)
            else:
                # reactivate only
                self.ble_object.active(True)
        else:
            # TODO: more to handle there
            self.ble_object.active(False)
        gc.collect()

    def tick(self):
        # every 10ms
        if self.BLE:
            self.i = (self.i + 1) % 1000
            if self.i % 100 == 0:
                # print("LOG: t", self.i)
                t = urandom.randint(10, 20)
                try:
                    self.ble_object.set_temperature(t, notify=self.i==0)
                except Exception as e:
                    print("E:BLE:{}".format(e))

    def toggle_wifi(self):
        self.WIFI = not self.WIFI

    def toggle_contrast(self):
        self.contrast_index += 1
        if self.contrast_index >= len(self.contrasts):
            self.contrast_index = 0
        self.backlight.duty(self.contrasts[self.contrast_index])
        print("LOG: Contrast", self.contrasts[self.contrast_index])


class Engine(BaseEngine):
    
    def __init__(self):
        super().__init__()
        self.version = __version__
        self.core = CoreEngine()

    def cmd_TOP(self, *params):
        stat = statvfs('/')  # Internal Flash
        blocksize = stat[0]
        fragsize = stat[1]
        fragfs = stat[2]
        freeblocks = stat[3]
        fs_size = fragfs * fragsize / 1024  # In KB
        free_size = blocksize * freeblocks / 1024  # In Kb
        print("W:TOP:FS={}/{} Kb:RAM={}/{} Kb".format(fs_size - free_size, fs_size, gc.mem_alloc(), gc.mem_free()+gc.mem_alloc()))

    """
    def _tick(self):
        self.core.tick()
        while stdin in select([stdin], [], [], 0)[0]:
            ch = stdin.read(1)
            if ord(ch) > 27:
                self.command_buffer += ch
                self.parent.ui.reverse_flash()
            elif ord(ch) ==10:
                print("CMD: {}".format(self.command_buffer))
                self.parent.status_text(self.command_buffer)
                if self.command_buffer.startswith('W:'):
                    segments = self.command_buffer.split(":")[1:]
                    command = "cmd_{}".format(segments.pop(0))
                    try:
                        test = getattr(self, command)
                        test(segments)
                    except Exception as e:
                        print("E:{}".format(e))
                self.command_buffer = ''
    """
