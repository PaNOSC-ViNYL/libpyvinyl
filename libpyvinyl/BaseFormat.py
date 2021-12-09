from abc import abstractmethod
from libpyvinyl.AbstractBaseClass import AbstractBaseClass
from libpyvinyl.BaseData import BaseData
import numpy as np


class BaseFormat(AbstractBaseClass):
    """The abstract format class. It's the interface of a certain data format."""
    def __init__(self):
        # This class is not designed in a object-oriented model, rather a collection of functions.
        pass

    @classmethod
    @abstractmethod
    def format_register(self):
        # Redefine this `format_register` method for a concrete format class.
        key = 'Base'
        desciption = 'Base data format'
        file_extension = 'base'
        read_kwargs = ['']
        write_kwargs = ['']
        return self._create_format_register(key, desciption, file_extension,
                                            read_kwargs, write_kwargs)

    @staticmethod
    @abstractmethod
    def direct_convert_formats():
        # Assume the format can be converted directly to the formats supported by these classes:
        # AFormat, BFormat
        # Redefine this `direct_convert_formats` for a concrete format class
        return [Aformat, BFormat]

    @classmethod
    def _create_format_register(cls,
                                key: str,
                                desciption: str,
                                file_extension: str,
                                read_kwargs=[''],
                                write_kwargs=['']):
        format_register = {
            'key': key,  # FORMAT KEY
            'description': desciption,  # FORMAT DISCRIPTION
            'ext': file_extension,  # FORMAT EXTENSION
            'format_class': cls,  # CLASS NAME OF THE FORMAT
            'read_kwargs': read_kwargs,  # KEYWORDS LIST NEEDED TO READ
            'write_kwargs': write_kwargs  # KEYWORDS LIST NEEDED TO WRITE
        }
        return format_register

    @classmethod
    @abstractmethod
    def read(self, filename: str, **kwargs) -> dict:
        """Read the data from the file with the `filename` to a dictionary. The dictionary will
        be used by its corresponding data class."""
        # Example codes. Redefine this function in a concrete class.
        data_dict = {}
        with h5py.File(filename, 'r') as h5:
            for key, val in h5.items():
                data_dict[key] = val[()]
        return data_dict

    @classmethod
    @abstractmethod
    def write(self, object: BaseData, filename: str, key: str, **kwargs):
        """Save the data with the `filename`."""
        # Example codes. Redefine this function in a concrete class.
        obj_key = key
        with h5py.File(filename, 'w') as h5:
            for key, val in object.get_data().items():
                h5[key] = val
        return object.from_file(filename, BaseData, obj_key)

    @classmethod
    @abstractmethod
    def convert(self, input: str, output: str, output_format_class: str, key,
                **kwargs):
        """Direct convert method, if the default converting would be too slow or not suitable for the output_format"""
        # If there is no direct converting supported:
        raise NotImplementedError
        if output_format_class is AFormat:
            return self.convert_to_AFormat(input, output, key)


class ExampleData(BaseData):
    """The simplest data class example"""
    def __init__(self,
                 key,
                 data_dict=None,
                 filename=None,
                 file_format_class=None,
                 file_format_kwargs=None):
        self.__expected_data = {}
        self.__expected_data['arr'] = np.zeros((1, 2))
        self.__expected_data['number'] = 1

        super().__init__(key,
                         self.__expected_data,
                         data_dict=data_dict,
                         filename=filename,
                         file_format_class=file_format_class,
                         file_format_kwargs=file_format_kwargs)

    @classmethod
    def supported_formats(self):
        format_dict = {}
        # Add the suppoted format classes when creating a concrete class.
        self._add_ioformat(format_dict, ExampleAFormat)
        self._add_ioformat(format_dict, ExampleBFormat)
        return format_dict


class ExampleAFormat(BaseFormat):
    """A format class of Example A"""
    def __init__(self):
        super().__init__()

    @classmethod
    def format_register(self):
        # Redefine this `format_register` method for a concrete format class.
        key = 'Example_A'
        desciption = 'Example A data format'
        file_extension = '.npz'
        read_kwargs = ['']
        write_kwargs = ['']
        return self._create_format_register(key, desciption, file_extension,
                                            read_kwargs, write_kwargs)

    @staticmethod
    def direct_convert_formats():
        # Assume the format can be converted directly to the formats supported by these classes:
        # AFormat, BFormat
        # Redefine this `direct_convert_formats` for a concrete format class
        return [ExampleBFormat]

    @classmethod
    def read(cls, filename: str) -> dict:
        """Read the data from the file with the `filename` to a dictionary. The dictionary will
        be used by its corresponding data class."""
        data_dict = np.load(filename)
        return data_dict

    @classmethod
    def write(cls, object: ExampleData, filename: str, key: str = None):
        """Save the data with the `filename`."""
        data_dict = object.get_data()
        arr = data_dict['arr']
        number = data_dict['number']
        np.savez(filename, arr=arr, number=number)
        if key is not None:
            return object.from_file(filename, cls, key)

    @classmethod
    def convert(cls,
                input: str,
                output: str,
                output_format_class: str,
                key=None,
                **kwargs):
        """Direct convert method, if the default converting would be too slow or not suitable for the output_format"""
        if output_format_class is ExampleBFormat:
            cls.convert_to_ExampleBFormat(input, output)
        else:
            raise TypeError(
                "Unsupported format {}".format(output_format_class))
        if key is not None:
            return ExampleData.from_file(output, output_format_class, key)

    @classmethod
    def convert_to_ExampleBFormat(cls, input: str, output: str):
        """The engine of convert method."""
        print("Converting ExampleA to ExampleB")
        data_dict = np.load(input)
        data = np.array([data_dict['arr'], np.zeros_like(data_dict['arr'])])
        data[1, :] = data_dict['number']
        np.save(output, data)


class ExampleBFormat(BaseFormat):
    """A format class of Example B"""
    def __init__(self):
        super().__init__()

    @classmethod
    def format_register(self):
        # Redefine this `format_register` method for a concrete format class.
        key = 'Example_B'
        desciption = 'Example B data format'
        file_extension = '.npy'
        read_kwargs = ['']
        write_kwargs = ['']
        return self._create_format_register(key, desciption, file_extension,
                                            read_kwargs, write_kwargs)

    @staticmethod
    def direct_convert_formats():
        # Assume the format can be converted directly to the formats supported by these classes:
        # AFormat, BFormat
        # Redefine this `direct_convert_formats` for a concrete format class
        return []
        return [ExampleAFormat]

    @classmethod
    def read(cls, filename: str) -> dict:
        """Read the data from the file with the `filename` to a dictionary. The dictionary will
        be used by its corresponding data class."""
        data_dict = {}
        data = np.load(filename)
        data_dict['arr'] = data[0]
        data_dict['number'] = np.ravel(data[1])[0]
        return data_dict

    @classmethod
    def write(cls, object: ExampleData, filename: str, key: str = None):
        """Save the data with the `filename`."""
        data_dict = object.get_data()
        data = np.array([data_dict['arr'], np.zeros_like(data_dict['arr'])])
        data[1, :] = data_dict['number']
        np.save(filename, data)
        if key is not None:
            return object.from_file(filename, cls, key)

    @classmethod
    def convert(cls, input: str, output: str, output_format_class: str, key,
                **kwargs):
        """Direct convert method, if the default converting would be too slow or not suitable for the output_format"""
        raise NotImplementedError


if __name__ == '__main__':
    data = {'arr': np.zeros((2, 3)), 'number': 1}
    # Python Dictionary mapping
    test1 = ExampleData.from_dict(data, key='test1')
    # Write the Python Dictionary in ExampleBFormat and create the data class object
    test1_dataB = test1.write('data.npy', ExampleBFormat, key='test1_dataB')
    # Write the file in ExampleAFormat without creating the data class object
    test1_dataB.write('data.npz', ExampleAFormat)
    # Write the file in ExampleAFormat creating the data class object test1_dataA
    test1_dataA = test1_dataB.write('data.npz',
                                    ExampleAFormat,
                                    key='test1_dataA')
    # Write the file in ExampleBFormat from ExampleAFormat
    test1_dataA.write('data_convert.npy', ExampleBFormat)
    # Write the file in ExampleBFormat from ExampleAFormat creating the data class object test1_convert
    test1_convert = test1_dataA.write('data_convert.npy',
                                      ExampleBFormat,
                                      key='test_convert')
    # print(test1_dataA.get_data())
    ExampleData.list_formats()
    print(test1)
    print(test1_convert)
