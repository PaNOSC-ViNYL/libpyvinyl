from libpyvinyl.BaseData import BaseData
from plusminus.ArrayData import TXTFormat, H5Format


class ArrayData(BaseData):
    def __init__(self,
                 key,
                 data_dict=None,
                 filename=None,
                 file_format_class=None,
                 file_format_kwargs=None):

        ### DataClass developer's job start
        expected_data = {}
        expected_data['array'] = None
        ### DataClass developer's job end

        super().__init__(key, expected_data, data_dict, filename,
                         file_format_class, file_format_kwargs)

    @classmethod
    def supported_formats(self):
        format_dict = {}
        ### DataClass developer's job start
        self.__add_ioformat(format_dict, TXTFormat)
        self.__add_ioformat(format_dict, H5Format)
        ### DataClass developer's job end
        return format_dict
