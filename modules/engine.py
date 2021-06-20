
__version__ = "0.1b"


class ComEngine:
    def __init__(self):
        pass

class Engine:
    
    def __init__(self):
        self.version = __version__
        self.crypto = None  # TODO: Crypto engine
        self.coms = ComEngine()
