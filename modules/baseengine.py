from sys import stdin
from select import select

__version__ = "0.1"

class BaseEngine:

    def __init__(self):
        self.version = __version__
        self.crypto = None
        self.parent = None
        self.command_buffer = ''
        self.core = None
        self.locked = True
        self.pins = []

    def unlock(self, pin):
        self.pins.append(pin)
        print("TODO: unlock")
        self.locked = False

    def lock(self):
        self.pins.clear()
        self.locked = True

    def cmd_PING(self, *params):
        print("PING: {}".format(params))
        print("W:PONG")

    def cmd_VERSION(self, *params):
        print("W:VERSION:{}".format(self.version))

    def cmd_ALS(self, *params):
        print("W:ALS:{}".format(params))
        print(params)

    def cmd_TOP(self, *params):
        print("W:TOP:N/A")

    def tick(self):
        if self.core:
            self.core.tick()
        while stdin in select([stdin], [], [], 0)[0]:
            ch = stdin.read(1)
            if ord(ch) > 27:
                self.command_buffer += ch
                self.parent.ui.reverse_flash()
            elif ord(ch) == 10:
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
