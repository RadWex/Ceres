# This Python file uses the following encoding: utf-8
import configparser
import pathlib


class SettingsMeta(type):
    """
    The Singleton meta class for settings instances
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Settings(metaclass=SettingsMeta):
    printerSettings = {
        "bed_size_x": '200',
        "bed_size_y": '200',
        "origin_x": '0',
        "origin_y": '0'
    }
    laserSettings = {
        "w": '0',
        "h": '40',
        "d": '0'
    }
    gcode = {
        "start": """G28 ; home all axes\nG1 Z5 F1500 ; lift nozzle""",
        "end": """G28 X0  ; home X axis\nM84 ; disable motors"""
    }

    def __init__(self):
        self.config = configparser.ConfigParser()
        file = pathlib.Path("config.ini")
        if not file.exists():
            self.create()
            print("File created")
        self.config.read(file)

        if self.config.has_section("printer settings"):
            for key, val in self.config.items("printer settings"):
                if key in self.printerSettings and self.is_number(val):
                    self.printerSettings[key] = val
        if self.config.has_section("G-code"):
            for key, val in self.config.items("G-code"):
                if key in self.gcode:
                    self.gcode[key] = val

    def save(self):
        pass

    def create(self):
        self.config.add_section('printer settings')
        for key in self.printerSettings.keys():
            self.config.set('printer settings', key, self.printerSettings[key])
        self.config.add_section('G-code')
        for key in self.gcode.keys():
            self.config.set('G-code', key, self.gcode[key])
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def is_number(self, s):
        s = s.replace(',', '.')
        try:
            float(s)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    s = Settings()
    print(s.printerSettings)
