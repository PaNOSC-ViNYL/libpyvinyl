from abc import abstractmethod
from libpyvinyl.AbstractBaseClass import AbstractBaseClass
from libpyvinyl.BaseData import BaseData


class BaseFormat(AbstractBaseClass):
    """The abstract format class. It's the interface of a certain data format."""

    def __init__(self):
        # Nothing needs to be done here.
        pass

    @classmethod
    @abstractmethod
    def format_register(self):
        # Redefine this `format_register` method for a concrete format class.
        key = "Base"
        desciption = "Base data format"
        file_extension = "base"
        read_kwargs = [""]
        write_kwargs = [""]
        return self._create_format_register(
            key, desciption, file_extension, read_kwargs, write_kwargs
        )

    @classmethod
    def _create_format_register(
        cls,
        key: str,
        desciption: str,
        file_extension: str,
        read_kwargs=[""],
        write_kwargs=[""],
    ):
        format_register = {
            "key": key,  # FORMAT KEY
            "description": desciption,  # FORMAT DESCRIPTION
            "ext": file_extension,  # FORMAT EXTENSION
            "format_class": cls,  # CLASS NAME OF THE FORMAT
            "read_kwargs": read_kwargs,  # KEYWORDS LIST NEEDED TO READ
            "write_kwargs": write_kwargs,  # KEYWORDS LIST NEEDED TO WRITE
        }
        return format_register

    @classmethod
    @abstractmethod
    def read(self, filename: str, **kwargs) -> dict:
        """Read the data from the file with the `filename` to a dictionary. The dictionary will
        be used by its corresponding data class."""
        # Example codes. Redefine this function in a concrete class.
        data_dict = {}
        with h5py.File(filename, "r") as h5:
            for key, val in h5.items():
                data_dict[key] = val[()]
        return data_dict

    @classmethod
    @abstractmethod
    def write(self, object: BaseData, filename: str, key: str, **kwargs):
        """Save the data with the `filename`."""
        # Example codes. Redefine this function in a concrete class.
        obj_key = key
        with h5py.File(filename, "w") as h5:
            for key, val in object.get_data().items():
                h5[key] = val
        return object.from_file(filename, BaseData, obj_key)

    @staticmethod
    @abstractmethod
    def direct_convert_formats():
        # Assume the format can be converted directly to the formats supported by these classes:
        # AFormat, BFormat
        # Redefine this `direct_convert_formats` for a concrete format class
        return [Aformat, BFormat]

    @classmethod
    @abstractmethod
    def convert(
        cls, obj: BaseData, output: str, output_format_class: str, key, **kwargs
    ):
        """Direct convert method, if the default converting would be too slow or not suitable for the output_format"""
        # If there is no direct converting supported:
        raise NotImplementedError
        if output_format_class is AFormat:
            return cls.convert_to_AFormat(obj.filename, output)
        else:
            raise TypeError(
                "Direct converting to format {} is not supported".format(
                    output_format_class
                )
            )
        # Set the key of the returned object
        if key is None:
            original_key = obj.key
            key = original_key + "_from_BaseFormat"
            return obj.from_file(output, output_format_class, key)
        else:
            return obj.from_file(output, output_format_class, key)

    # Example convert_to_AFormat()
    # @classmethod
    # def convert_to_AFormat(cls, input: str, output: str):
    #     """The engine of convert method."""
    #     print("Directly converting BaseFormat to AFormat")
    #     number = float(np.loadtxt(input))
    #     with h5py.File(output, "w") as h5:
    #         h5["number"] = number
