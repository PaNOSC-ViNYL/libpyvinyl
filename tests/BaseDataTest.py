from libpyvinyl.BaseData import BaseData, DataCollection
from libpyvinyl.BaseFormat import BaseFormat
import numpy as np
import h5py


class ExampleData(BaseData):
    """The simplest data class example"""
    def __init__(self,
                 key,
                 data_dict=None,
                 filename=None,
                 file_format_class=None,
                 file_format_kwargs=None):
        super().__init__(key,
                         data_dict=data_dict,
                         filename=filename,
                         file_format_class=file_format_class,
                         file_format_kwargs=file_format_kwargs)
        self.__expected_data['arr'] = np.zeros((1, 2))
        self.__expected_data['number'] = 1

    def supported_formats(self):
        format_dict = {}
        # Add the suppoted format classes when creating a concrete class.
        # See the example at xx
        self.__add_ioformat(format_dict, ExampleFormat)
        return format_dict


class ExampleFormat(BaseFormat):
    def __init__(self):
        self.__format_register = {
            'key': 'test',  # FORMAT KEY
            'description': 'Test data format',  # FORMAT DISCRIPTION
            'ext': '.h5',  # FORMAT EXTENSION
            'format_class': 'TestFormat',  # CLASS NAME OF THE FORMAT
            'read_kwargs': [''],  # KEYWORDS LIST NEEDED TO READ
            'write_kwargs': ['']  # KEYWORDS LIST NEEDED TO WRITE
        }
        self.__direct_convert_formats = []

    @property
    def format_register(self):
        return self.__format_register

    @property
    def direct_convert_formats(self):
        return self.__direct_convert_formats

    @classmethod
    def read(self, filename: str):
        """Read the data from the file with the `filename`. It returns an instance of the data class"""
        data_dict = {}
        with h5py.File(filename, 'r') as h5:
            for key, val in h5.items():
                data_dict[key] = val
        return data_dict

    @classmethod
    def write(self, object: BaseData, filename: str, key: str):
        """Save the data object with the `filename`."""
        obj_key = key
        with h5py.File(filename, 'w') as h5:
            for key, val in object.get_data().items():
                h5[key] = val
        return TestData.from_file(filename, TestFormat, obj_key)

    @classmethod
    def convert(self, input: str, output: str, output_format: str, key,
                **kwargs):
        """Direct convert method, if the default converting would be too slow or not suitable for the output_format"""
        raise NotImplementedError()


class Test2Format(BaseFormat):
    def __init__(self):
        self.__format_register = {
            'key': 'test2',  # FORMAT KEY
            'description': 'Test data format2',  # FORMAT DISCRIPTION
            'ext': '.h5',  # FORMAT EXTENSION
            'format_class': 'Test2Format',  # CLASS NAME OF THE FORMAT
            'read_kwargs': [''],  # KEYWORDS LIST NEEDED TO READ
            'write_kwargs': ['']  # KEYWORDS LIST NEEDED TO WRITE
        }
        self.__direct_convert_formats = [TestFormat]

    # Should be in base foramt
    @property
    def format_register(self):
        return self.__format_register

    # Should be in base foramt
    @property
    def direct_convert_formats(self):
        return self.__direct_convert_formats

    @classmethod
    def read(self, filename: str):
        """Read the data from the file with the `filename`. It returns an instance of the data class"""
        data_dict = {}
        with h5py.File(filename, 'r') as h5:
            for key, val in h5.items():
                data_dict[key] = val[()]
        return data_dict

    @classmethod
    def write(self, object: BaseData, filename: str, key: str):
        """Save the data object with the `filename`."""
        obj_key = key
        with h5py.File(filename, 'w') as h5:
            for key, val in object.get_data().items():
                h5[key] = val
            h5['format'] = 'Test2Format'
        return TestData.from_file(filename, Test2Format, obj_key)

    @classmethod
    def convert(self, input: str, output: str, output_format_class: str, key,
                **kwargs):
        """Direct convert method, if the default converting would be too slow or not suitable for the output_format"""
        if output_format_class is TestFormat:
            return self.convert_to_TestFormat(input, output, key)

    @classmethod
    def convert_to_TestFormat(self, input: str, output: str, key):
        """Direct convert method, if the default converting would be too slow or not suitable for the output_format"""
        obj_key = key
        with h5py.File(input, 'r') as h5_in:
            with h5py.File(output, 'w') as h5_out:
                for key, val in h5_in.items():
                    if key != 'format':
                        h5_out[key] = val[()]
        return TestData.from_file(output, TestFormat, obj_key)


class TestData(BaseData):
    """The abstract wrapper data class. It's designed in a way so that its inheritance is an API of a
    kind of data (e.g. wavefront, sample, and diffraction) rather than that of a certain data format."""
    def __init__(self,
                 key,
                 data_dict=None,
                 filename=None,
                 file_format_class=None,
                 file_format_kwargs=None):
        self.__key = key
        excepted_data = {}
        excepted_data['arr'] = [1, 1]
        excepted_data['number'] = 2
        self.__expected_data = excepted_data
        self.__ioformats = {}
        self._add_ioformat(TestFormat)
        self._add_ioformat(Test2Format)

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

    @property
    def ioformats(self):
        return self.__ioformats

    def _add_ioformat(self, format_class):
        format_class_obj = format_class()
        for key, val in format_class_obj.format_register.items():
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

    # Should be in base data
    @classmethod
    def from_file(cls, filename: str, format_class, key, **kwargs):
        """Create the data class by the file in the `format`."""
        return cls(key,
                   filename=filename,
                   file_format_class=format_class,
                   file_format_kwargs=kwargs)

    # Should be in base data
    @classmethod
    def from_dict(cls, data_dict, key):
        """Create the data class by a python dictionary."""
        return cls(key, data_dict=data_dict)

    def write(self, filename: str, format_class, key, **kwargs):
        # From either a file or a python object to a file
        # The behaviour related to a file will always be handled by
        # the format class.
        """Save the data with the `filename` in the `format`."""
        if self.mapping_type == 'Python Dictionary':
            return format_class.write(self, filename, key, **kwargs)
        elif format_class == self.__file_format_class:
            pass
        else:
            self.__file_format_class.convert(self.__filename, filename,
                                             format_class, key, **kwargs)

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


data = {'arr': np.zeros((2, 3)), 'number': 1}
td1 = TestData.from_dict(data, key='wavefront1')
data = {'arr': np.zeros((3, 3)), 'number': 2}
td2 = TestData.from_dict(data, key='wavefront2')
td2_file = td2.write('wavefront2.h5', TestFormat, key='wavefront2_file')
td2_new_format = td2.write('wavefront2_newformat.h5',
                           Test2Format,
                           key='wavefront2_newformat')
td1_convert = td2_new_format.write(
    'wavefront2_convert.h5',
    TestFormat,
    key='wavefront2_convert_from_Test2Format.h5')

collection = DataCollection(td1, td2, td2_file, td2_new_format)
print(td1)
print(collection)
subset = collection['wavefront1']
print(subset)
td_object = subset.get_data_object('wavefront1')
print(td_object.get_data())
