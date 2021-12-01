from abc import abstractmethod
from libpyvinyl.AbstractBaseClass import AbstractBaseClass
from importlib import import_module


class BaseData(AbstractBaseClass):
    """The abstract wrapper data class. It's designed in a way so that its inheritance is an API of a
    kind of data (e.g. wavefront, sample, and diffraction) rather than that of a certain data format."""
    @abstractmethod
    def __init__(self):
        self._ioformats = {
            'UNKNOWN': {  # FORMAT KEY
                'description': 'UNKNOWN data format',  # FORMAT DISCRIPTION
                'ext': '',  # FORMAT EXTENSION
                'module': '',  # API MODULE NAME OF THE FORMAT
                'read_kwargs': [''],  # KEYWORDS LIST NEEDED TO READ
                'write_kwargs': ['']  # KEYWORDS LIST NEEDED TO WRITE
            }
        }

    @property
    def ioformats(self):
        return self._ioformats

    def _add_ioformat(self, key: str, description: str, ext: str,
                      read_kwargs: list, write_kwargs: list):
        self._ioformats[key]['description'] = description
        self._ioformats[key]['ext'] = ext
        self._ioformats[key]['read_kwargs'] = read_kwargs
        self._ioformats[key]['write_kwargs'] = write_kwargs

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
            module = dicts['module']
            if module != '':
                out_string += 'API module: {}\n'.format(module)
            kwargs = dicts['read_kwargs']
            if kwargs != ['']:
                out_string += 'Extra reading keywords: {}\n'.format(kwargs)
            kwargs = dicts['write_kwargs']
            if kwargs != ['']:
                out_string += 'Extra writing keywords: {}\n'.format(kwargs)
            out_string += '\n'
        print(out_string)

    @classmethod
    def read(self, filename: str, format: str, **kwargs):
        """Read the data from the file with the `filename` in the `format`. It returns an instance of the data class"""
        module_name = self._ioformats[format]['module']
        data_module = import_module(module_name)
        return data_module.read(filename, **kwargs)

    def write(self, filename: str, format: str, **kwargs):
        """Save the data with the `filename` in the `format`."""
        module_name = self._ioformats[format]['module']
        data_module = import_module(module_name)
        data_module.write(self, filename, **kwargs)

    @classmethod
    @abstractmethod
    def convert(self, input_filename, input_format, output_filename,
                output_format, **kwargs):
        """Convert a file into another format"""
        module_name = self._ioformats[input_format]['module']
        data_module = import_module(module_name)
        # If there is a direct converter
        if data_module.convert(input_filename, output_filename, output_format,
                               **kwargs):
            pass
        else:
            data_obj = self.read(input_filename, input_format)
            out_module_name = self._ioformats[input_format]['module']
            out_data_module = import_module(out_module_name)
            out_data_module.write(data_obj, output_filename, **kwargs)


class BaseFormat(AbstractBaseClass):
    """The abstract format class. It's the interface of a certain data format."""
    @abstractmethod
    def __init__(self):
        self.__format_register = {
            'base': {  # FORMAT KEY
                'description': 'Base data format',  # FORMAT DISCRIPTION
                'ext': 'base',  # FORMAT EXTENSION
                'module':
                'libpyvinyl.BaseData.BaseFormat',  # API MODULE NAME OF THE FORMAT
                'read_kwargs': [''],  # KEYWORDS LIST NEEDED TO READ
                'write_kwargs': ['']  # KEYWORDS LIST NEEDED TO WRITE
            }
        }
        self.__direct_convert_formats = ['format_key_01', 'format_key_02']

    @property
    def format_register(self):
        return self.__format_register

    @classmethod
    @abstractmethod
    def read(self, filename: str, **kwargs) -> BaseData:
        """Read the data from the file with the `filename`. It returns an instance of the data class"""
        return BaseData()

    @classmethod
    @abstractmethod
    def write(self, object: BaseData, filename: str, **kwargs):
        """Save the data with the `filename`."""
        pass

    @classmethod
    @abstractmethod
    def convert(self, input: str, output: str, output_format: str, **kwargs):
        """Direct convert method, if the default converting would be too slow or not suitable for the output_format"""
        if output_format in self.__direct_convert_formats:
            # self.format_convert(input, input, output_format)
            return True
        else:
            return False


# class ExampleData(BaseData):
#     def __init__(self):
#         super().__init__()
#         # self.listFormats()

#     def read(self, filename: str, format: str):

#     def write(self):
#         pass

#     def convert(self):
#         pass
