from abc import abstractmethod
from libpyvinyl.AbstractBaseClass import AbstractBaseClass
from libpyvinyl.BaseData import BaseData


class BaseFormat(AbstractBaseClass):
    """The abstract format class. It's the interface of a certain data format."""
    @abstractmethod
    def __init__(self):
        self.__format_register = {
            'key': 'Base',  # FORMAT KEY
            'description': 'Base data format',  # FORMAT DISCRIPTION
            'ext': 'base',  # FORMAT EXTENSION
            'format_class': 'BaseFormat',  # CLASS NAME OF THE FORMAT
            'read_kwargs': [''],  # KEYWORDS LIST NEEDED TO READ
            'write_kwargs': ['']  # KEYWORDS LIST NEEDED TO WRITE
        }
        # The formats can be directly converted to this format.
        self.__direct_convert_formats = ['format_key_01', 'format_key_02']

    @property
    def format_register(self):
        return self.__format_register

    @property
    def direct_convert_formats(self):
        return self.__direct_convert_formats

    @classmethod
    @abstractmethod
    def read(self, filename: str, **kwargs) -> BaseData:
        """Read the data from the file with the `filename`. It returns an instance of the data class"""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def write(self, object: BaseData, filename: str, **kwargs):
        """Save the data with the `filename`."""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def convert(self, input: str, output: str, output_format: str, **kwargs):
        """Direct convert method, if the default converting would be too slow or not suitable for the output_format"""
        if output_format in self.__direct_convert_formats:
            # self.format_convert(input, input, output_format)
            return True
        else:
            return False
