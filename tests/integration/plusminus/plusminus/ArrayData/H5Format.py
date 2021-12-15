import h5py
from libpyvinyl.BaseFormat import BaseFormat
from plusminus.ArrayData import ArrayData


class H5Format(BaseFormat):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def format_register(self):
        key = 'H5'
        desciption = 'H5 format for ArrayData'
        file_extension = '.h5'
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
        with h5py.File(filename, 'r') as h5:
            array = h5['array'][()]
        data_dict = {'array': array}
        return data_dict

    @classmethod
    def write(cls, object: ArrayData, filename: str, key: str = None):
        """Save the data with the `filename`."""
        data_dict = object.get_data()
        array = data_dict['array']
        with h5py.File(filename, 'w') as h5:
            h5['array'] = array
        if key is None:
            original_key = object.key
            key = original_key + '_to_H5Format'
            return object.from_file(filename, cls, key)
        else:
            return object.from_file(filename, cls, key)
