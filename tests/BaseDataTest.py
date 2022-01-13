from libpyvinyl.BaseData import BaseData, DataCollection
from libpyvinyl.BaseFormat import BaseFormat
import numpy as np
import h5py


class NumberData(BaseData):
    def __init__(
        self,
        key,
        data_dict=None,
        filename=None,
        file_format_class=None,
        file_format_kwargs=None,
    ):

        ### DataClass developer's job start
        expected_data = {}
        expected_data["number"] = None
        ### DataClass developer's job end

        super().__init__(
            key,
            expected_data,
            data_dict,
            filename,
            file_format_class,
            file_format_kwargs,
        )

    @classmethod
    def supported_formats(self):
        format_dict = {}
        ### DataClass developer's job start
        self._add_ioformat(format_dict, TXTFormat.TXTFormat)
        self._add_ioformat(format_dict, H5Format.H5Format)
        ### DataClass developer's job end
        return format_dict


class TXTFormat(BaseFormat):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def format_register(self):
        key = "TXT"
        desciption = "TXT format for NumberData"
        file_extension = ".txt"
        read_kwargs = [""]
        write_kwargs = [""]
        return self._create_format_register(
            key, desciption, file_extension, read_kwargs, write_kwargs
        )

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
        data_dict = {"number": number}
        return data_dict

    @classmethod
    def write(cls, object: NumberData, filename: str, key: str = None):
        """Save the data with the `filename`."""
        data_dict = object.get_data()
        arr = np.array([data_dict["number"]])
        np.savetxt(filename, arr, fmt="%.3f")
        if key is None:
            original_key = object.key
            key = original_key + "_to_TXTFormat"
            return object.from_file(filename, cls, key)
        else:
            return object.from_file(filename, cls, key)


class H5Format(BaseFormat):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def format_register(self):
        key = "H5"
        desciption = "H5 format for NumberData"
        file_extension = ".h5"
        read_kwargs = [""]
        write_kwargs = [""]
        return self._create_format_register(
            key, desciption, file_extension, read_kwargs, write_kwargs
        )

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
        with h5py.File(filename, "r") as h5:
            number = h5["number"][()]
        data_dict = {"number": number}
        return data_dict

    @classmethod
    def write(cls, object: NumberData, filename: str, key: str = None):
        """Save the data with the `filename`."""
        data_dict = object.get_data()
        number = data_dict["number"]
        with h5py.File(filename, "w") as h5:
            h5["number"] = number
        if key is None:
            original_key = object.key
            key = original_key + "_to_H5Format"
            return object.from_file(filename, cls, key)
        else:
            return object.from_file(filename, cls, key)


def test_create_empty_data_instance():
    number_data = NumberData()
