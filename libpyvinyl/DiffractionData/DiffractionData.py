from libpyvinyl.BaseData import BaseData
from importlib import import_module


# Define the data needed to connect the calculator.
class DiffractionData(BaseData):
    def __init__(self, array, distance):
        super().__init__()
        self.__array = array
        self.__distance = distance
        self._add_ioformat(self._ioformats, 'simple',
                           'Simple example data format', '.h5',
                           'libpyvinyl.DiffractionData.SimpleFormat',
                           'SimpleFormat')

    @property
    def array(self):
        return self.__array

    @property
    def distance(self):
        return self.__distance

    @classmethod
    def read(self, filename: str, format, **kwargs):
        """Read the data from the file with the `filename` in the `format`. It returns an instance of the data class"""

        return format.read(filename, **kwargs)
