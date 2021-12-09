from abc import abstractmethod
from libpyvinyl.AbstractBaseClass import AbstractBaseClass


class BaseData(AbstractBaseClass):
    # It represents a python object
    """The abstract wrapper data class. It's designed in a way so that its inheritance is an API of a
    kind of data (e.g. wavefront, sample, and diffraction) rather than that of a certain data format."""
    @abstractmethod
    def __init__(self,
                 key,
                 data_dict=None,
                 filename=None,
                 file_format_class=None,
                 file_format_kwargs=None):
        self.__key = key
        excepted_data = {}
        excepted_data['data1'] = 1
        excepted_data['data2'] = 2
        self.__expected_data = excepted_data
        self.__ioformats = {}
        self._add_ioformat(openPMDFormat)
        self._add_ioformat(singfelFormat)

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
    def ioformats(self):
        return self.__ioformats

    @property
    def mapping_type(self):
        if self.__data_dict is not None:
            return 'Python Dictionary'
        elif self.__filename is not None:
            return 'Data file: {}'.format(self.__filename)
        else:
            raise TypeError(
                'Niether self.__data_dict or self.__filename was found.')

    def _add_ioformat(self, format_class):
        for key, val in format_class.items():
            if key == 'key':
                this_format = val
                self.__ioformats[val] = {}
            else:
                self.__ioformats[this_format][key] = val

    def listFormats(self):
        """Print supported formats"""
        out_string = ''
        for key in self.ioformats:
            dicts = self.ioformats[key]
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

    @classmethod
    def from_file(cls, filename: str, format_class, **kwargs):
        """Create the data class by the file in the `format`."""
        return cls(filename=filename,
                   file_format_class=format_class,
                   file_format_kwargs=kwargs)

    @classmethod
    def from_dict(cls, data_dict):
        """Create the data class by a python dictionary."""
        return cls(data_dict=data_dict)

    def write(self, filename: str, format_class, **kwargs):
        # From either a file or a python object to a file
        # The behaviour related to a file will always be handled by
        # the format class.
        """Save the data with the `filename` in the `format`."""
        return format_class.write(self, filename, **kwargs)

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

    def __getitem__(self, *keys):
        subset = []
        for key in keys:
            subset.append(self.data_object_dict[key])
        return DataCollection(*subset)

    def add_data(self, *args):
        """Add data objects to the data colletion"""
        for data in args:
            self.data_object_dict[data.key] = data

    def get_data_object(self, key):
        return self.data_object_dict[key]

    def to_list(self):
        """Export a list of the data objects in the data colletion"""
        return [self.data_object_dict[key] for key in self.data_dict.keys()]

    def __repr__(self):
        """Returns strings of Data objets info"""
        string = ''
        for data_object in self.data_object_dict.values():
            string += str(data_object)
        return string
