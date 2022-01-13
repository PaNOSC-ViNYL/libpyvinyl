from libpyvinyl.BaseData import BaseData
from plusminus.NumberData import TXTFormat, H5Format


class NumberData(BaseData):
    def __init__(
        self,
        key,
        data_dict=None,
        filename=None,
        file_format_class=None,
        file_format_kwargs=None,
    ):

        ### DataClass developer's job start
        expected_data = {}
        expected_data["number"] = None
        ### DataClass developer's job end

        super().__init__(
            key,
            expected_data,
            data_dict,
            filename,
            file_format_class,
            file_format_kwargs,
        )

    @classmethod
    def supported_formats(self):
        format_dict = {}
        ### DataClass developer's job start
        self._add_ioformat(format_dict, TXTFormat.TXTFormat)
        self._add_ioformat(format_dict, H5Format.H5Format)
        ### DataClass developer's job end
        return format_dict

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
