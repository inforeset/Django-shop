from pathlib import Path
import yaml


class SettingFileLoader:

    def __init__(self, file):
        self.__file = file

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, value):
        if not Path(value).exists():
            raise FileExistsError
        self.__file = value

    @property
    def config(self):
        with open(Path(self.__file)) as file_settings:
            return yaml.safe_load(file_settings)
