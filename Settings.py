# This Python file uses the following encoding: utf-8
from PySide2.QtCore import Signal
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
    a = Signal(float, float)
    printerSettings = {
        "default"
    }
    default = {
        "bed_size_x": '200',
        "bed_size_y": '200',
        "origin_x": '0',
        "origin_y": '0',
        "w": '0',
        "h": '40',
        "d": '0'
    }
    activePrinterPreset = 'default'
    gcode = {
        "start": """G28 ; home all axes\nG1 Z5 F1500 ; lift nozzle""",
        "end": """G28 X0  ; home X axis\nM84 ; disable motors"""
    }

    listOfPrinterPresets = {}

    def __init__(self):
        self.config = configparser.ConfigParser(allow_no_value=True)
        file = pathlib.Path("config.ini")
        if not file.exists():
            self.create()
            print("File created")
        self.config.read(file)

        if self.config.has_section("printer settings"):
            for name_of_settings, _ in self.config.items("printer settings"):
                data = {}
                for key, val in self.config.items(name_of_settings):
                    data[key] = val
                self.listOfPrinterPresets[name_of_settings] = data
        # if self.config.has_section("printer settings"):
        #     for key, val in self.config.items("printer settings"):
        #         if key in self.printerSettings and self.is_number(val):
        #             self.printerSettings[key] = val
        if self.config.has_section("G-code"):
            for key, val in self.config.items("G-code"):
                if key in self.gcode and self.is_number(val):
                    self.gcode[key] = val
        if self.config.has_section("last printer preset"):
            key = self.config.items("last printer preset")
            self.activePrinterPreset = key[0][0]

    def save_printer_preset_name(self, name):
        if self.config.has_section("printer settings"):
            self.config.add_section(name)
            self.config.set('printer settings', name)
            for key in self.default.keys():
                self.config.set(name, key, self.default[key])
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)

    def save_printer_preset(self, settings: dict):
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

    def get_printer_preset_by_name(self, name) -> dict:
        for i in self.listOfPrinterPresets.keys():
            if i == name:
                return i
        print('[ERROR]Settings not found')

    def is_number(self, s):
        s = s.replace(',', '.')
        try:
            float(s)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    s = Settings()
    # print(s.printerSettings)
    # print(f'{s.listOfPrinterPresets}')
    # print(s.get_printer_settings_by_name('test'))
    print(s.listOfPrinterPresets[s.activePrinterPreset])
