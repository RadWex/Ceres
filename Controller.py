from PyQt5.QtCore import QObject


class ControllerMeta(type):
    """
    The Singleton meta class for controller instances
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Controller(metaclass=ControllerMeta):
    signals = {}
    slots = {}

    def __init__(self):
        pass

    def addSend(self, name, signal):
        # print(name)
        self.signals[signal] = name
        # self.match()

    def addRecive(self, name, slot):
        self.slots[slot] = name
        # self.match()

    def match(self):
        for k, v in self.signals.items():
            for k2, v2 in self.slots.items():
                if v == v2:
                    #print(v, ' ', v2)
                    k.connect(k2)

    def showConnections(self):
        for k, v in self.signals.items():
            for k2, v2 in self.slots.items():
                if v == v2:
                    print(v, '<->', v2)


if __name__ == "__main__":
    s = Controller()
    s2 = Controller()
    print(s.printerSettings)
