import pytest
import numpy as np
import h5py
from libpyvinyl.BaseData import BaseData
from libpyvinyl.BaseFormat import BaseFormat


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


@pytest.fixture()
def txt_file(tmp_path_factory):
    fn_path = tmp_path_factory.mktemp("test_data") / "test.txt"
    txt_file = str(fn_path)
    with open(txt_file, "w") as f:
        f.write("4")
    return txt_file


# Data class section
def test_create_empty_data_instance():
    """Test creating an empty data instance"""
    with pytest.raises(TypeError):
        number_data = NumberData()
    test_data = NumberData(key="test_data")
    assert isinstance(test_data, NumberData)


def test_create_data_with_set_dict():
    """Test set dict after in an empty data instance"""
    test_data = NumberData(key="test_data")
    my_dict = {"number": 4}
    test_data.set_dict(my_dict)
    assert test_data.get_data()["number"] == 4


def test_create_data_with_set_file(txt_file):
    """Test set file after in an empty data instance"""
    test_data = NumberData(key="test_data")
    test_data.set_file(txt_file, TXTFormat)
    assert test_data.get_data()["number"] == 4


def test_create_data_with_set_file_wrong_param(txt_file):
    """Test set file after in an empty data instance with wrong `format_class` param"""
    test_data = NumberData(key="test_data")
    with pytest.raises(TypeError):
        test_data.set_file(txt_file, "txt")


def test_create_data_with_set_file_wrong_format(txt_file):
    """Test set file after in an empty data instance with wrong `format_class`"""
    test_data = NumberData(key="test_data")
    test_data.set_file(txt_file, H5Format)
    with pytest.raises(OSError):
        test_data.get_data()


def test_create_data_with_file():
    """Test set dict after in  an empty data instance"""
    test_data = NumberData(key="test_data")
    assert isinstance(test_data, NumberData)
    my_dict = {"number": 4}
    test_data.set_dict(my_dict)
    assert test_data.get_data()["number"] == 4


def test_create_data_from_dict():
    """Test creating a data instance from a dict"""
    my_dict = {"number": 4}
    test_data = NumberData.from_dict(my_dict, "test_data")


def test_check_key_from_dict():
    """Test checking expected data key from dict"""
    my_dict = {"number": 4}
    test_data = NumberData.from_dict(my_dict, "test_data")
    test_data.get_data()
    my_dict = {"numberr": 4}
    test_data = NumberData.from_dict(my_dict, "test_data")
    with pytest.raises(KeyError):
        test_data.get_data()


def test_create_data_from_file_wrong_param(txt_file):
    """Test creating a data instance from a file in a wrong file format type"""
    with pytest.raises(TypeError):
        test_data = NumberData.from_file(txt_file, "txt", "test_data")


def test_create_data_from_TXTFormat(txt_file):
    """Test creating a data instance from a file in TXTFormat"""
    test_data = NumberData.from_file(txt_file, TXTFormat, "test_data")
    assert test_data.get_data()["number"] == 4


def test_create_data_from_wrong_format(txt_file):
    """Test creating a data instance from a file in TXTFormat"""
    test_data = NumberData.from_file(txt_file, H5Format, "test_data")
    with pytest.raises(OSError):
        test_data.get_data()


def test_save_dict_data_in_TXTFormat(tmpdir):
    """Test saving a dict data in TXTFormat"""
    my_dict = {"number": 4}
    test_data = NumberData.from_dict(my_dict, "test_data")
    fn = str(tmpdir / "test.txt")
    test_data.write(fn, TXTFormat)
    read_data = NumberData.from_file(fn, TXTFormat, "read_data")
    assert read_data.get_data()["number"] == 4


def test_save_dict_data_in_TXTFormat_return_data_object(tmpdir):
    """Test saving a dict data in TXTFormat returning data object with default key"""
    my_dict = {"number": 4}
    test_data = NumberData.from_dict(my_dict, "test_data")
    fn = str(tmpdir / "test.txt")
    return_data = test_data.write(fn, TXTFormat)
    assert return_data.get_data()["number"] == 4
    assert return_data.key == "test_data_to_TXTFormat"


def test_save_dict_data_in_TXTFormat_return_data_object_key(tmpdir):
    """Test saving a dict data in TXTFormat returning data object with custom key"""
    my_dict = {"number": 4}
    test_data = NumberData.from_dict(my_dict, "test_data")
    print(test_data)
    # assert False
    fn = str(tmpdir / "test.txt")
    return_data = test_data.write(fn, TXTFormat, "custom")
    assert return_data.get_data()["number"] == 4
    assert return_data.key == "custom"


def test_save_file_data_in_another_format(txt_file, tmpdir):
    """Test saving a TXTFormat data in H5Format"""
    test_data = NumberData.from_file(txt_file, TXTFormat, "test_data")
    print(test_data)
    fn = str(tmpdir / "test.h5")
    return_data = test_data.write(fn, H5Format)
    print(return_data)
    # assert False

#TODO:
# test_list_formats
# test_collections