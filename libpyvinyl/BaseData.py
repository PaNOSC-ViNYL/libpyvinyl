""" :module BaseData: Module hosts the BaseData class."""
from abc import abstractmethod, ABCMeta
from libpyvinyl.AbstractBaseClass import AbstractBaseClass


class BaseData(AbstractBaseClass):
    """The abstract data class. Inheriting classes represent simulation input and/or output
    data and provide a harmonized user interface to simulation data of various kinds rather than a data format.
    Their purpose is to provide a harmonized user interface to common data operations such as reading/writing from/to disk."""

    def __init__(
        self,
        key,
        expected_data,
        data_dict=None,
        filename=None,
        file_format_class=None,
        file_format_kwargs=None,
    ):
        self.__key = None
        self.__expected_data = None
        self.__data_dict = None
        self.__filename = None
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

        self.__check_consistensy()

    @property
    def key(self):
        """The key of the class instance for calculator usage"""
        return self.__key

    @key.setter
    def key(self, value):
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

    def set_dict(self, data_dict):
        self.data_dict = data_dict

    def set_file(self, filename: str, format_class, **kwargs):
        self.filename = filename
        self.file_format_class = format_class
        self.file_format_kwargs = kwargs

    @property
    def filename(self):
        """The filename of the class instance for calculator usage"""
        return self.__filename

    @filename.setter
    def filename(self, value):
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
        """The file_format_class of the class instance for calculator usage"""
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
        """The file_format_class of the class instance for calculator usage"""
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
        """mapping_type returns if this data class is a file mapping or python dict mapping."""
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
        # See the example at xx
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
            if format_class != "":
                out_string += "Format class: {}\n".format(format_class)
            out_string += f"Key: {key}\n"
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

    def __check_consistensy(self):
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
    def from_file(cls, filename: str, format_class, key, **kwargs):
        """Create the data class by the file in the `format`."""
        return cls(
            key,
            filename=filename,
            file_format_class=format_class,
            file_format_kwargs=kwargs,
        )

    @classmethod
    def from_dict(cls, data_dict, key):
        """Create the data class by a python dictionary."""
        return cls(key, data_dict=data_dict)

    def write(self, filename: str, format_class, key=None, **kwargs):
        # From either a file or a python object to a file
        # The behavior related to a file will always be handled by
        # the format class.
        """Save the data with the `filename` in the `format`."""
        # If it's a python dictionary mapping, write with the specified format_class
        # directly.
        if self.mapping_type == dict:
            return format_class.write(self, filename, key, **kwargs)
        elif format_class in self.__file_format_class.direct_convert_formats():
            return self.__file_format_class.convert(
                self.__filename, filename, format_class, key, **kwargs
            )
        # If it's a file mapping and would like to write in the same file format of the
        # mapping, it will let the user know that a file containing the data in the same format already existed.
        elif format_class == self.__file_format_class:
            print(
                f"Hint: This data already existed in the file {self.__filename} in format {self.__file_format_class}. `cp {self.__filename} {filename}` could be faster."
            )
            print(
                f"Will still write the data into the file {filename} in format {format_class}"
            )
            return format_class.write(self, filename, key, **kwargs)
        else:
            return format_class.write(self, filename, key, **kwargs)

    def __get_dict_data(self):
        # python object to python object
        if self.__data_dict is not None:
            data_to_return = self.__expected_data.copy()
            # It will automatically check the data needed to be extracted.
            for key in data_to_return.keys():
                try:
                    data_to_return[key] = self.__data_dict[key]
                except KeyError:
                    raise KeyError(
                        f"Expected data dict key '{key}' is not found."
                    ) from None
            return data_to_return
        else:
            raise RuntimeError("__get_dict_data() should not be called when self.__data_dict is None")

    def __get_file_data(self):
        # file to python object
        if self.__filename is not None:
            data_to_return = self.__expected_data.copy()
            data_to_read = self.__file_format_class.read(
                self.__filename, **self.__file_format_kwargs
            )
            # It will automatically check the data needed to be extracted.
            for key in data_to_return.keys():
                data_to_return[key] = data_to_read[key]
            return data_to_return
        else:
            raise RuntimeError("__get_file_data() should not be called when self.__filename is None")

    def get_data(self):
        """Return the data in a dictionary"""
        # From either a file or a python object to a python object
        if self.__data_dict is not None:
            return self.__get_dict_data()
        elif self.__filename is not None:
            return self.__get_file_data()

    def __str__(self):
        """Returns strings of Data objects info"""
        string = f"key = {self.key}\n"
        string += f"mapping = {self.mapping_type}: {self.mapping_content}"
        return string


# DataCollection class
class DataCollection:
    def __init__(self, *args):
        self.data_object_dict = {}
        self.add_data(*args)

    def __len__(self):
        return len(self.data_object_dict)

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
            self.data_object_dict[data.key] = data

    def get_data(self):
        """When there is only one item in the DataCollection"""
        if len(self.data_object_dict) == 1:
            for obj in self.data_object_dict.values():
                return obj.get_data()
        else:
            raise RuntimeError(
                f"More than 1 data object in this DataCollection: {self.data_object_dict.keys()}.\nPick one of them to get_data()"
            )

    def write(self, filename: str, format_class, key=None, **kwargs):
        """When there is only one item in the DataCollection"""
        if len(self.data_object_dict) == 1:
            for obj in self.data_object_dict.values():
                return obj.write(filename, format_class, key, **kwargs)
        else:
            raise RuntimeError(
                f"More than 1 data object in this DataCollection: {self.data_object_dict.keys()}.\nPick one of them to write()"
            )

    def get_data_object(self, key):
        return self.data_object_dict[key]

    def to_list(self):
        """Export a list of the data objects in the data collection"""
        return [value for value in self.data_object_dict.values()]

    def __str__(self):
        """Returns strings of Data objects info"""
        string = "Data collection:\n"
        string = "key - mapping_type\n\n"
        for data_object in self.data_object_dict.values():
            string += f"{data_object.key} - {data_object.mapping_type}\n"
        return string
