import numpy as np
from libpyvinyl.BaseFormat import BaseFormat
from plusminus.NumberData import NumberData


class TXTFormat(BaseFormat):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def format_register(self):
        key = 'TXT'
        desciption = 'TXT format for NumberData'
        file_extension = '.txt'
        read_kwargs = ['']
        write_kwargs = ['']
        return self._create_format_register(key, desciption, file_extension,
                                            read_kwargs, write_kwargs)

    @staticmethod
    def direct_convert_formats():
        # Assume the format can be converted directly to the formats supported by these classes:
        # AFormat, BFormat
        # Redefine this `direct_convert_formats` for a concrete format class
        return []

    @classmethod
    def read(cls, filename: str) -> dict:
        """Read the data from the file with the `filename` to a dictionary. The dictionary will
        be used by its corresponding data class."""
        number = float(np.loadtxt(filename))
        data_dict = {'number': number}
        return data_dict

    @classmethod
    def write(cls, object: NumberData, filename: str, key: str = None):
        """Save the data with the `filename`."""
        data_dict = object.get_data()
        arr = np.array([data_dict['number']])
        np.savetxt(filename, arr, fmt='%.3f')
        if key is None:
            original_key = object.key
            key = original_key + '_to_TXTFormat'
            return object.from_file(filename, cls, key)
        else:
            return object.from_file(filename, cls, key)
