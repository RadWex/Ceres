import inspect
from PySide2.QtCore import QObject


class ControllerDebug():
    def __init__(self, signals, slots):
        self.signals = signals
        self.slots = slots
        self.connected = []
        self.get_connected()

    def printConnected(self):
        #[print(y) for x, y in self.signals.values()]
        col_len = [8, 11, 7]
        col_len[0] = max(len(endpoint)
                         for endpoint, class_name in self.signals.values())
        col_len[1] = max(len(class_name)
                         for endpoint, class_name in self.signals.values())
        col_len[2] = max(len(class_name) + len(fun.__name__)
                         for fun, (endpoint, class_name) in self.slots.items())
        # print(col_len[0])

        print(
            f'{"endpoint".center(col_len[0])} | {"signal from".center(col_len[1])}  |  {"to slot".center(col_len[2])}')
        print("=" * (col_len[0]+col_len[1]+col_len[2]+9))

        for k, v in self.signals.items():
            for k2, v2 in self.slots.items():
                if v[0] == v2[0]:
                    print(
                        f'{v[0]:{col_len[0]}} | {v[1]:{col_len[1]}} -> {v2[1]}.{k2.__name__}')
        print("=" * (col_len[0]+col_len[1]+col_len[2]+9))

    def printSignals(self):
        col_len = [8, 11, 7]
        col_len[0] = max(len(endpoint)
                         for endpoint, class_name in self.signals.values())
        col_len[1] = max(len(class_name)
                         for endpoint, class_name in self.signals.values())
        col_len[2] = max(len(class_name) + len(fun.__name__)
                         for fun, (endpoint, class_name) in self.slots.items())
        print()
        print('NOT connected SIGNALS:')
        print(
            f'{"endpoint".center(col_len[0])} | {"signal from".center(col_len[1])}  |  {"to slot".center(col_len[2])}')
        print("=" * (col_len[0]+col_len[1]+col_len[2]+9))

        for k, v in self.signals.items():
            unconnected = True
            for i in self.connected:
                if v[0] == i:
                    unconnected = False
                    break
            if unconnected:
                print(
                    f'{v[0]:{col_len[0]}} | {v[1]:{col_len[1]}}  |  {"-".center(col_len[2])}')

    def printSlots(self):
        col_len = [8, 11, 7]
        col_len[0] = max(len(endpoint)
                         for endpoint, class_name in self.slots.values())
        col_len[1] = max(len(class_name)
                         for endpoint, class_name in self.slots.values())
        col_len[2] = max(len(class_name) + len(fun.__name__)
                         for fun, (endpoint, class_name) in self.slots.items())
        print()
        print('NOT connected SLOTS:')
        print(
            f'{"endpoint".center(col_len[0])} | {"signal from".center(col_len[1])}  |  {"to slot".center(col_len[2])}')
        print("=" * (col_len[0]+col_len[1]+col_len[2]+9))
        for k, v in self.slots.items():
            unconnected = True
            for i in self.connected:
                if v[0] == i:
                    unconnected = False
                    break
            if unconnected:
                print(
                    f'{v[0]:{col_len[0]}} | {"-".center(col_len[1])}  |  {v[1]}.{k.__name__}')

    def get_connected(self):
        for k, v in self.signals.items():
            for k2, v2 in self.slots.items():
                if v[0] == v2[0]:
                    self.connected.append(v[0])


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
        # ONLY FOR DEBUG
        # get the call frame of the calling method
        caller = None
        frame = inspect.currentframe().f_back
        try:
            # try to access the caller's "self"
            try:
                self_obj = frame.f_locals['self']
            except KeyError:
                pass

            # get the class of the "self" and return its name
            caller = type(self_obj).__name__
        finally:
            # clean up the frame at the end to avoid ref cycles
            del frame
        # ONLY FOR DEBUG END

        self.signals[signal] = (name, caller)

    def addRecive(self, name, slot):
        # ONLY FOR DEBUG
        # get the call frame of the calling method
        caller = None
        frame = inspect.currentframe().f_back
        try:
            # try to access the caller's "self"
            try:
                self_obj = frame.f_locals['self']
            except KeyError:
                pass

            # get the class of the "self" and return its name
            caller = type(self_obj).__name__
        finally:
            # clean up the frame at the end to avoid ref cycles
            del frame
        # ONLY FOR DEBUG END

        self.slots[slot] = (name, caller)

    def match(self):
        # connecting signals and slots
        for k, v in self.signals.items():
            for k2, v2 in self.slots.items():
                if v[0] == v2[0]:
                    k.connect(k2)

    def addTempSend(self, name, signal):
        """signal is not added to dict; 
            slot must be already in dict; 
            disconnect signal after use;
            use for temporary windows"""
        for k, v in self.slots.items():
            if name == v[0]:
                signal.connect(k)

    def showConnections(self):
        debug = ControllerDebug(self.signals, self.slots)
        debug.printConnected()
        debug.printSignals()
        debug.printSlots()

    def logConnections(self):
        pass


if __name__ == "__main__":
    s = Controller()
    s2 = Controller()
    print(s.printerSettings)
