import h5py
from libpyvinyl.BaseFormat import BaseFormat
from libpyvinyl.BaseData import BaseData
from libpyvinyl.DiffractionData import DiffractionData


class SimpleFormat(BaseFormat):
    def __init__(self):
        super().__init__()
        self.__direct_convert_formats = ['']

    @classmethod
    def read(self, filename: str) -> DiffractionData:
        """Read the data from the file with the `filename`. It returns an instance of the data class"""
        with h5py.File(filename, 'r') as h5:
            array = h5['array'][()]
            distance = h5['distance'][()]
        return DiffractionData(array, distance)

    @classmethod
    def write(self, object: DiffractionData, filename: str):
        with h5py.File(filename, 'w') as h5:
            h5['array'] = object.array
            h5['distance'] = object.distance

    @classmethod
    def convert(self, input: str, output: str, output_format: str, **kwargs):
        raise NotImplementedError
