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
                'format_class': '',  # API MODULE NAME OF THE FORMAT
                'read_kwargs': [''],  # KEYWORDS LIST NEEDED TO READ
                'write_kwargs': ['']  # KEYWORDS LIST NEEDED TO WRITE
            }
        }

    @property
    def ioformats(self):
        return self._ioformats

    @staticmethod
    def _add_ioformat(ioformats,
                      key: str,
                      description: str,
                      ext: str,
                      module: str,
                      format_class: str,
                      read_kwargs=[''],
                      write_kwargs=['']):
        ioformats[key] = {}
        ioformats[key]['description'] = description
        ioformats[key]['ext'] = ext
        ioformats[key]['module'] = module
        ioformats[key]['format_class'] = format_class
        ioformats[key]['read_kwargs'] = read_kwargs
        ioformats[key]['write_kwargs'] = write_kwargs

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
    def read(self, filename: str, format_class, **kwargs):
        """Read the data from the file with the `filename` in the `format`. It returns an instance of the data class"""
        # module_name = self._ioformats[format]['module']
        # format_class = self._ioformats[format]['format_class']
        # data_class = getattr(import_module(module_name), format_class)
        ## This should work if read is a classmethod
        return format_class.read(filename, **kwargs)

    def write(self, filename: str, format_class, **kwargs):
        """Save the data with the `filename` in the `format`."""
        return format_class.write(self, filename, **kwargs)

        module_name = self._ioformats[format]['module']
        format_class = self._ioformats[format]['format_class']
        data_class = getattr(import_module(module_name), format_class)
        data_class.write(self, filename, **kwargs)

    @classmethod
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


