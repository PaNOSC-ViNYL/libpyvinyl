""" :module BaseData: Module hosts the BaseData class."""
from typing import Union, Optional
from abc import abstractmethod, ABCMeta
from libpyvinyl.AbstractBaseClass import AbstractBaseClass


class BaseData(AbstractBaseClass):
    """The abstract data class.
    Inheriting classes represent simulation input and/or output
    data and provide a harmonized user interface to simulation data of various kinds rather than a data format.
    Their purpose is to provide a harmonized user interface to common data operations such as reading/writing from/to disk.
    """

    def __init__(
        self,
        key: str,
        expected_data: dict,
        data_dict: Optional[dict] = None,
        filename: Optional[str] = None,
        file_format_class=None,
        file_format_kwargs: Optional[dict] = None,
    ):
        """
        :param key: The key to identify the Data Object.
        :param expected_data: A placeholder dict for expected data. The keys of this dict are expected to be found during the execution of `get_data()`.
                              The value for each key can be `None`.
        :param data_dict: The dict to map by this DataClass. It has to be `None` if a file mapping was already set, defaults to None.

        :param filename: The filename of the file to map by this DataClass. It has to be `None` if a dict mapping was already set, defaults to None.

        :param file_format_class: The FormatClass to map the file by this DataClass, It has to be `None` if a dict mapping was already set, defaults to None
        :type file_format_class: class, optional
        :param file_format_kwargs: The kwargs needed to map the file, defaults to None.
        """
        self.__key = None
        self.__expected_data = None
        self.__data_dict = None
        self.__filename: Optional[str] = None
        self.__file_format_class = None
        self.__file_format_kwargs = None

        self.key = key
        # Expected_data is checked when `self.get_data()`
        self.expected_data = expected_data
        # This will be always be None if the data class is mapped to a file
        self.data_dict = data_dict
        # These will be always be None if the data class is mapped to a python data dict object
        self.filename = filename
        self.file_format_class = file_format_class
        self.file_format_kwargs = file_format_kwargs

        self.__check_consistency()

    @property
    def key(self) -> str:
        """The key of the class instance for calculator usage"""
        return self.__key

    @key.setter
    def key(self, value: str):
        if isinstance(value, str):
            self.__key = value
        else:
            raise TypeError(f"Data Class: key should be a str, not {type(value)}")

    @property
    def expected_data(self):
        """The expected_data of the class instance for calculator usage"""
        return self.__expected_data

    @expected_data.setter
    def expected_data(self, value):
        if isinstance(value, dict):
            self.__expected_data = value
        else:
            raise TypeError(
                f"Data Class: expected_data should be a dict, not {type(value)}"
            )

    @property
    def data_dict(self):
        """The data_dict of the class instance for calculator usage"""
        return self.__data_dict

    @data_dict.setter
    def data_dict(self, value):
        if isinstance(value, dict):
            self.__data_dict = value
        elif value is None:
            self.__data_dict = None
        else:
            raise TypeError(
                f"Data Class: data_dict should be None or a dict, not {type(value)}"
            )
        self.__check_consistency()

    def set_dict(self, data_dict: dict):
        """Set a mapping dict for this DataClass.

        :param data_dict: The data dict to map
        :type data_dict: dict
        """
        self.data_dict = data_dict

    def set_file(self, filename: str, format_class, **kwargs):
        """Set a mapping file for this DataClass.

        :param filename: The filename of the file to map.
        :param format_class: The FormatClass to map the file
        :type format_class: class
        """
        self.filename = filename
        self.file_format_class = format_class
        self.file_format_kwargs = kwargs
        self.__check_consistency()

    @property
    def filename(self) -> Optional[str]:
        """The filename of the file to map by this DataClass."""
        return self.__filename

    @filename.setter
    def filename(self, value: Optional[str]):
        if isinstance(value, str):
            self.__filename = value
        elif value is None:
            self.__filename = None
        else:
            raise TypeError(
                f"Data Class: filename should be None or a str, not {type(value)}"
            )

    @property
    def file_format_class(self):
        """The FormatClass to map the file by this DataClass"""
        return self.__file_format_class

    @file_format_class.setter
    def file_format_class(self, value):
        if isinstance(value, ABCMeta):
            self.__file_format_class = value
        elif value is None:
            self.__file_format_class = None
        else:
            raise TypeError(
                f"Data Class: format_class should be None or a format class, not {type(value)}"
            )

    @property
    def file_format_kwargs(self):
        """The kwargs needed to map the file"""
        return self.__file_format_kwargs

    @file_format_kwargs.setter
    def file_format_kwargs(self, value):
        if isinstance(value, dict):
            self.__file_format_kwargs = value
        elif value is None:
            self.__file_format_kwargs = None
        else:
            raise TypeError(
                f"Data Class: file_format_kwargs should be None or a dict, not {type(value)}"
            )

    @property
    def mapping_type(self):
        """If this data class is a file mapping or python dict mapping."""
        return self.__check_mapping_type()

    def __check_mapping_type(self):
        """Check the mapping_type of this class."""
        if self.data_dict is not None:
            return dict
        elif self.filename is not None:
            return self.file_format_class
        else:
            raise TypeError("Neither self.__data_dict or self.__filename was found.")

    @property
    def mapping_content(self):
        """Returns an overview of the keys of the mapped dict or the filename of the mapped file"""
        if self.mapping_type == dict:
            return self.data_dict.keys()
        else:
            return self.filename

    @staticmethod
    def _add_ioformat(format_dict, format_class):
        """Register an ioformat to a `format_dict` listing the formats supported by this DataClass.

        :param format_dict: The dict listing the supported formats.
        :type format_dict: dict
        :param format_class: The FormatClass to add.
        :type format_class: class
        """
        register = format_class.format_register()
        for key, val in register.items():
            if key == "key":
                this_format = val
                format_dict[val] = {}
            else:
                format_dict[this_format][key] = val

    @classmethod
    @abstractmethod
    def supported_formats(self):
        format_dict = {}
        # Add the supported format classes when creating a concrete class.
        # See the example at `tests/BaseDataTest.py`
        self._add_ioformat(format_dict, FormatClass)
        return format_dict

    @classmethod
    def list_formats(self):
        """Print supported formats"""
        out_string = ""
        supported_formats = self.supported_formats()
        for key in supported_formats:
            dicts = supported_formats[key]
            format_class = dicts["format_class"]
            if format_class:
                out_string += "Format class: {}\n".format(format_class)
            out_string += "Key: {}\n".format(key)
            out_string += "Description: {}\n".format(dicts["description"])
            ext = dicts["ext"]
            if ext != "":
                out_string += "File extension: {}\n".format(ext)
            kwargs = dicts["read_kwargs"]
            if kwargs != [""]:
                out_string += "Extra reading keywords: {}\n".format(kwargs)
            kwargs = dicts["write_kwargs"]
            if kwargs != [""]:
                out_string += "Extra writing keywords: {}\n".format(kwargs)
            out_string += "\n"
        print(out_string)

    def __check_consistency(self):
        # If all of the file-related parameters are set:
        if all([self.filename, self.file_format_class]):
            # If the data_dict is also set:
            if self.data_dict is not None:
                raise RuntimeError(
                    "self.data_dict and self.filename can not be set for one data class at the same time."
                )
            else:
                pass
        # If any one of the file-related parameters is None:
        elif (
            self.filename is None
            and self.file_format_class is None
            and self.file_format_kwargs is None
        ):
            pass
        # If some of the file-related parameters is None and some is not None:
        else:
            raise RuntimeError(
                "self.filename, self.file_format_class, self.file_format_kwargs are not consistent."
            )

    @classmethod
    def from_file(cls, filename: str, format_class, key: dict, **kwargs):
        """Create a Data Object mapping a file.

        :param filename: The filename of the file to map by this DataClass. It has to be `None` if a dict mapping was already set, defaults to None.
        :type filename: str, optional
        :param file_format_class: The FormatClass to map the file by this DataClass, It has to be `None` if a dict mapping was already set, defaults to None
        :type file_format_class: class, optional
        :param file_format_kwargs: The kwargs needed to map the file, defaults to None.
        :type file_format_kwargs: dict, optional
        :param key: The key to identify the Data Object.
        :type key: str

        :return: A Data Object
        :rtype: BaseData
        """
        return cls(
            key,
            filename=filename,
            file_format_class=format_class,
            file_format_kwargs=kwargs,
        )

    @classmethod
    def from_dict(cls, data_dict: dict, key: str):
        """Create a Data Object mapping a data dict.

        :param data_dict: The dict to map by this DataClass. It has to be `None` if a file mapping was already set, defaults to None.
        :type data_dict: dict
        :param key: The key to identify the Data Object.
        :type key: str
        :return: A Data Object
        :rtype: BaseData
        """
        return cls(key, data_dict=data_dict)

    def write(self, filename: str, format_class, key: str = None, **kwargs):
        """Write the data mapped by the Data Object into a file and return a Data Object
        mapping the file. It converts either a file or a python object to a file
        The behavior related to a file will always be handled by the format class.
        If it's a python dictionary mapping, write with the specified format_class
        directly.

        :param filename: The filename of the file to be written.
        :type filename: str
        :param file_format_class: The FormatClass to write the file.
        :type file_format_class: class
        :param key: The identification key of the new Data Object. When it's `None`, a new key will
        be generated with a suffix added to the previous identification key by the FormatClass. Defaults to None.
        :type key: str, optional
        :return: A Data Object
        :rtype: BaseData
        """
        if self.mapping_type == dict:
            return format_class.write(self, filename, key, **kwargs)
        elif format_class in self.file_format_class.direct_convert_formats():
            return self.file_format_class.convert(
                self, filename, format_class, key, **kwargs
            )
        # If it's a file mapping and would like to write in the same file format of the
        # mapping, it will let the user know that a file containing the data in the same format already existed.
        elif format_class == self.file_format_class:
            print(
                f"Hint: This data already existed in the file {self.__filename} in format {self.__file_format_class}. `cp {self.__filename} {filename}` could be faster."
            )
            print(
                f"Will still write the data into the file {filename} in format {format_class}"
            )
            return format_class.write(self, filename, key, **kwargs)
        else:
            return format_class.write(self, filename, key, **kwargs)

    def __check_for_expected_data(self, data_to_read):
        """Check if the `data_to_read` contains the data we have"""
        for key in self.expected_data.keys():
            try:
                data_to_read[key]
            except KeyError:
                raise KeyError(
                    f"Expected data dict key '{key}' is not found."
                ) from None

    def __get_dict_data(self):
        """Get the data dict from a dict mapping"""
        if self.__data_dict is not None:
            # It will automatically check the data needed to be extracted.
            self.__check_for_expected_data(self.__data_dict)
            return self.data_dict
        else:
            raise RuntimeError(
                "__get_dict_data() should not be called when self.__data_dict is None"
            )

    def __get_file_data(self, **kwargs):
        """Get the data dict from a file mapping"""
        if self.__filename is not None:
            data_to_read = self.__file_format_class.read(
                self.__filename, **self.__file_format_kwargs, **kwargs
            )
            # It will automatically check the data needed to be extracted.
            self.__check_for_expected_data(data_to_read)
            data_to_return = {}
            for key in data_to_read.keys():
                data_to_return[key] = data_to_read[key]
            return data_to_return
        else:
            raise RuntimeError(
                "__get_file_data() should not be called when self.__filename is None"
            )

    def get_data(self, **kwargs):
        """Return the data in a dictionary"""
        # From either a file or a python object to a python object
        if self.__data_dict is not None:
            return self.__get_dict_data()
        elif self.__filename is not None:
            return self.__get_file_data(**kwargs)
        else:
            raise RuntimeError("Cannot read the data from either a dict or a file.")

    def __str__(self):
        """Returns strings of Data objects info"""
        string = f"key = {self.key}\n"
        string += f"mapping = {self.mapping_type}: {self.mapping_content}"
        return string


# DataCollection class
class DataCollection:
    """A collection of Data Objects"""

    def __init__(self, *args):
        self.data_object_dict = {}
        self.add_data(*args)

    def __len__(self):
        return len(self.data_object_dict)

    def __setitem__(self, key, value):
        if key != value.key:
            print(
                f"Warning: the key '{key}' of this DataCollection will be replaced by the key '{value.key}' set in the input data."
            )
        del self.data_object_dict[key]
        self.add_data(value)

    def __getitem__(self, keys):
        if isinstance(keys, str):
            return self.get_data_object(keys)
        elif isinstance(keys, list):
            subset = []
            for key in keys:
                subset.append(self.get_data_object(key))
            return DataCollection(*subset)

    def add_data(self, *args):
        """Add data objects to the data colletion"""
        for data in args:
            assert isinstance(data, BaseData)
            self.data_object_dict[data.key] = data

    def get_data(self):
        """Get the data of the data object(s).
        When there is only one item in the DataCollection, it returns the data dict,
        When there are more then one items, it returns a dictionary of the data dicts"""
        if len(self.data_object_dict) == 1:
            return next(iter(self.data_object_dict.values())).get_data()
        else:
            data_dicts = {}
            for key, obj in self.data_object_dict.items():
                data_dicts[key] = obj.get_data()
            return data_dicts

    def write(
        self,
        filename: Union[str, dict],
        format_class,
        key: Union[str, dict] = None,
        **kwargs,
    ):
        """Write the data object(s) to the file(s).
        When there is only one item in the DataCollection, it returns the data object mapping the file which was wirttern,
        When there are more then one items, it returns a dictionary of the data objects.

        :param filename: The name(s) of the file(s) to write. When there are multiple items, they are expected in
        a dict where the keys corresponding to the data in this collection.
        :type filename: str or dict
        :param format_class: The format class of the file(s). When there are multiple items, they are expected in
        a dict where the keys corresponding to the data in this collection.
        :type format_class: class or dict
        :param key: The key(s) of the data object(s) mapping the written file(s), defaults to None.
        :type key: str or dict, optional
        :return: A data object or a dict of data objects.
        :rtype: DataClass or dict
        """

        if len(self.data_object_dict) == 1:
            obj = next(iter(self.data_object_dict.values()))
            return obj.write(filename, format_class, key, **kwargs)
        else:
            assert isinstance(key, dict)
            data_dicts = {}
            for col_key, obj in self.data_object_dict.items():
                written_data = obj.write(
                    filename[col_key], format_class[col_key], key[col_key], **kwargs
                )
                data_dicts[written_data.key] = written_data
            return data_dicts

    def get_data_object(self, key: str):
        """Get one data object by its key

        :param key: The key of the data object to get.
        :type key: str
        :return: A data object
        :rtype: DataClass
        """
        return self.data_object_dict[key]

    def to_list(self):
        """Return a list of the data objects in the data collection"""
        return [value for value in self.data_object_dict.values()]

    def __str__(self):
        """Returns strings of the data object info"""
        string = "Data collection:\n"
        string += "key - mapping\n\n"
        for data_object in self.data_object_dict.values():
            string += f"{data_object.key} - {data_object.mapping_type}: {data_object.mapping_content}\n"
        return string
