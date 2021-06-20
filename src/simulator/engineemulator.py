from baseengine import BaseEngine


__version__ = "0.1c-EMUL"


class CoreEngine:
    def __init__(self):
        self.BLE = False
        self.WIFI = False
        self.contrasts = [50,100,150,200,250]
        self.contrast_index = 1
        self.contrast = self.contrasts[self.contrast_index]

    def toggle_ble(self):
        self.BLE = not self.BLE

    def toggle_wifi(self):
        self.WIFI = not self.WIFI

    def toggle_contrast(self):
        self.contrast_index += 1
        if self.contrast_index >= len(self.contrasts):
            self.contrast_index = 0
        self.contrast = self.contrasts[self.contrast_index]

    def tick(self):
        pass


class Engine(BaseEngine):
    
    def __init__(self):
        super().__init__()
        self.version = __version__
        self.core = CoreEngine()
