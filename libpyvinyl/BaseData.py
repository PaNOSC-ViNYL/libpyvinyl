""" :module BaseData: Module hosts the BaseData class."""
from abc import abstractmethod
from libpyvinyl.AbstractBaseClass import AbstractBaseClass


class BaseData(AbstractBaseClass):
    # It represents a python object
    """The abstract wrapper data class. It's designed in a way so that its inheritance is an API of a
    kind of data (e.g. wavefront, sample, and diffraction) rather than that of a certain data format."""
    def __init__(self,
                 key,
                 expected_data,
                 data_dict=None,
                 filename=None,
                 file_format_class=None,
                 file_format_kwargs=None):
        self.__key = key
        self.__expected_data = expected_data

        # This will be always be None if the data class is mapped to a file
        self.__data_dict = data_dict
        # These will be always be None if the data class is mapped to a python data dict object
        self.__filename = filename
        self.__file_format_class = file_format_class
        self.__file_format_kwargs = file_format_kwargs

    @property
    def key(self):
        """The key of the class instance for calculator usage"""
        return self.__key

    @property
    def mapping_type(self):
        if self.__data_dict is not None:
            return 'Python Dictionary'
        elif self.__filename is not None:
            return 'Data file: {}'.format(self.__filename)
        else:
            raise TypeError(
                'Niether self.__data_dict or self.__filename was found.')

    @staticmethod
    def _add_ioformat(format_dict, format_class):
        register = format_class.format_register()
        for key, val in register.items():
            if key == 'key':
                this_format = val
                format_dict[val] = {}
            else:
                format_dict[this_format][key] = val

    @classmethod
    @abstractmethod
    def supported_formats(self):
        format_dict = {}
        # Add the suppoted format classes when creating a concrete class.
        # See the example at xx
        self._add_ioformat(format_dict, FormatClass)
        return format_dict

    @classmethod
    def list_formats(self):
        """Print supported formats"""
        out_string = ''
        supported_formats = self.supported_formats()
        for key in supported_formats:
            dicts = supported_formats[key]
            out_string += f'Key: {key}\n'
            out_string += 'Description: {}\n'.format(dicts['description'])
            ext = dicts['ext']
            if ext != '':
                out_string += 'File extension: {}\n'.format(ext)
            format_class = dicts['format_class']
            if format_class != '':
                out_string += 'Format class: {}\n'.format(format_class)
            kwargs = dicts['read_kwargs']
            if kwargs != ['']:
                out_string += 'Extra reading keywords: {}\n'.format(kwargs)
            kwargs = dicts['write_kwargs']
            if kwargs != ['']:
                out_string += 'Extra writing keywords: {}\n'.format(kwargs)
            out_string += '\n'
        print(out_string)

    def set_file(self, filename: str, format_class, key, **kwargs):
        self.__key = key
        self.__filename = filename
        self.__file_format_class = format_class
        self.__file_format_kwargs = kwargs

    @classmethod
    def from_file(cls, filename: str, format_class, key, **kwargs):
        """Create the data class by the file in the `format`."""
        return cls(key,
                   filename=filename,
                   file_format_class=format_class,
                   file_format_kwargs=kwargs)

    def set_dict(self, data_dict, key):
        self.__key = key
        self.__data_dict = data_dict

    @classmethod
    def from_dict(cls, data_dict, key):
        """Create the data class by a python dictionary."""
        return cls(key, data_dict=data_dict)

    def write(self, filename: str, format_class, key=None, **kwargs):
        # From either a file or a python object to a file
        # The behaviour related to a file will always be handled by
        # the format class.
        """Save the data with the `filename` in the `format`."""
        # If it's a python dictionary mapping, write with the specified format_class
        # directly.
        if self.mapping_type == 'Python Dictionary':
            return format_class.write(self, filename, key, **kwargs)
        elif format_class in self.__file_format_class.direct_convert_formats():
            return self.__file_format_class.convert(self.__filename, filename,
                                                    format_class, key,
                                                    **kwargs)
        # If it's a file mapping and would like to write in the same fileformat of the
        # mapping, it will let the user know that a file containing the data in the same format already existed.
        elif format_class == self.__file_format_class:
            print(
                f"Hint: This data already existed in the file {self.__filename} in format {self.__file_format_class}. `cp {self.__filename} {filename}` could be faster."
            )
            print(
                f"Will still write the data into the file {filename} in format {format_class}"
            )
        # The default behaviour is to read the data into a dict and write it to a file.
        return format_class.write(self, filename, key, **kwargs)

    def get_dict_data(self):
        # python object to python object
        if self.__data_dict is not None:
            data_to_return = self.__expected_data.copy()
            # It will automatically check the data needed to be extracted.
            for key in data_to_return.keys():
                data_to_return[key] = self.__data_dict[key]
            return data_to_return

    def get_file_data(self):
        # file to python object
        if self.__filename is not None:
            data_to_return = self.__expected_data.copy()
            data_to_read = self.__file_format_class.read(
                self.__filename, **self.__file_format_kwargs)
            # It will automatically check the data needed to be extracted.
            for key in data_to_return.keys():
                data_to_return[key] = data_to_read[key]
            return data_to_return

    def get_data(self):
        """Return the data in a dictionary"""
        # From either a file or a python object to a python object
        if self.__data_dict is not None:
            return self.get_dict_data()
        elif self.__filename is not None:
            return self.get_file_data()

    def __repr__(self):
        """Returns strings of Data objets info"""
        string = ''
        string += self.key + ': ' + self.mapping_type + '\n'
        return string


# DataCollection class
class DataCollection():
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
        """Export a list of the data objects in the data colletion"""
        return [value for value in self.data_object_dict.values()]

    def __repr__(self):
        """Returns strings of Data objets info"""
        string = ''
        for data_object in self.data_object_dict.values():
            string += str(data_object)
        return string
