from dataclasses import dataclass


class DataMeta(type):
    """
    The Singleton meta class for data instances
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Data(metaclass=DataMeta):
    model = Model()

    def __init__(self):
        pass


@dataclass
class Model():
    path: str
