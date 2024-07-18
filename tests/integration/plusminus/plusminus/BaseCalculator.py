""" :module BaseCalculator: Module hosts the BaseData class."""

from abc import abstractmethod, ABCMeta
from typing import Union
from pathlib import Path
from libpyvinyl.AbstractBaseClass import AbstractBaseClass
from libpyvinyl.BaseData import BaseData, DataCollection
from libpyvinyl.Parameters import CalculatorParameters


class BaseCalculator(AbstractBaseClass):
    def __init__(
        self,
        name: str,
        input: Union[DataCollection, list, BaseData],
        output_keys: Union[list, str],
        output_data_types: list,
        output_filenames: Union[list, str],
        instrument_base_dir="./",
        calculator_base_dir="BaseCalculator",
        parameters: CalculatorParameters = None,
    ):
        """A python object calculator example"""
        # Initialize properties
        self.__name = None
        self.__instrument_base_dir = None
        self.__calculator_base_dir = None
        self.__input = None
        self.__input_keys = None
        self.__output_keys = None
        self.__output_data_types = None
        self.__output_filenames = None
        self.__parameters = None

        self.name = name
        self.input = input
        self.output_keys = output_keys
        self.output_data_types = output_data_types
        self.output_filenames = output_filenames
        self.instrument_base_dir = instrument_base_dir
        self.calculator_base_dir = calculator_base_dir
        self.parameters = parameters

        self.__init_output()

    @abstractmethod
    def init_parameters(self):
        raise NotImplementedError

    def __init_output(self):
        output = DataCollection()
        for i, key in enumerate(self.output_keys):
            output_data = self.output_data_types[i](key)
            output.add_data(output_data)
        self.output = output

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self.__name = value
        else:
            raise TypeError(
                f"Calculator: `name` is expected to be a str, not {type(value)}"
            )

    @property
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, value):
        if isinstance(value, CalculatorParameters):
            self.__parameters = value
        elif value is None:
            self.init_parameters()
        else:
            raise TypeError(
                f"Calculator: `parameters` is expected to be CalculatorParameters, not {type(value)}"
            )

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, value):
        self.set_input(value)

    def set_input(self, value: Union[DataCollection, list, BaseData]):
        if isinstance(value, DataCollection):
            self.__input = value
        elif isinstance(value, list):
            self.__input = DataCollection(*value)
        elif isinstance(value, BaseData):
            self.__input = DataCollection(value)
        else:
            raise TypeError(
                f"Calculator: `input` can be a  DataCollection, list or BaseData object, and will be treated as a DataCollection, but not {type(value)}"
            )

    @property
    def input_keys(self):
        return self.__input_keys

    @input_keys.setter
    def input_keys(self, value):
        self.set_input_keys(value)

    def set_input_keys(self, value: Union[list, str]):
        if isinstance(value, list):
            for item in value:
                assert type(item) is str
            self.__input_keys = value
        elif isinstance(value, str):
            self.__input_keys = [value]
        else:
            raise TypeError(
                f"Calculator: `input_keys` can be a list or a string, and will be treated as a list, but not {type(value)}"
            )

    @property
    def output_keys(self):
        return self.__output_keys

    @output_keys.setter
    def output_keys(self, value):
        self.set_output_keys(value)

    def set_output_keys(self, value: Union[list, str]):
        if isinstance(value, list):
            for item in value:
                assert type(item) is str
            self.__output_keys = value
        elif isinstance(value, str):
            self.__output_keys = [value]
        else:
            raise TypeError(
                f"Calculator: `output_keys` can be a list or a string, and will be treated as a list, but not {type(value)}"
            )

    @property
    def output_data_types(self):
        return self.__output_data_types

    @output_data_types.setter
    def output_data_types(self, value):
        self.set_output_data_types(value)

    def set_output_data_types(self, value):
        if isinstance(value, list):
            for item in value:
                assert type(item) is ABCMeta
            self.__output_data_types = value
        elif isinstance(value, ABCMeta):
            self.__output_data_types = [value]
        else:
            raise TypeError(
                f"Calculator: `output_data_types` can be a list or a DataClass, and will be treated as a list, but not {type(value)}"
            )

    @property
    def output_filenames(self):
        """Native calculator file names"""
        return self.__output_filenames

    @output_filenames.setter
    def output_filenames(self, value):
        self.set_output_filenames(value)

    def set_output_filenames(self, value: Union[list, str]):
        if isinstance(value, str):
            self.__output_filenames = [value]
        elif isinstance(value, list):
            self.__output_filenames = value
        else:
            raise TypeError(
                f"Calculator: `output_filenames` can to be a str or a list, and will be treated as a list, but not {type(value)}"
            )

    @property
    def instrument_base_dir(self):
        return self.__instrument_base_dir

    @instrument_base_dir.setter
    def instrument_base_dir(self, value):
        self.set_instrument_base_dir(value)

    def set_instrument_base_dir(self, value: str):
        if isinstance(value, str):
            self.__instrument_base_dir = value
        else:
            raise TypeError(
                f"Calculator: `instrument_base_dir` is expected to be a str, not {type(value)}"
            )

    @property
    def calculator_base_dir(self):
        return self.__calculator_base_dir

    @calculator_base_dir.setter
    def calculator_base_dir(self, value):
        self.set_calculator_base_dir(value)

    def set_calculator_base_dir(self, value: str):
        if isinstance(value, str):
            self.__calculator_base_dir = value
        else:
            raise TypeError(
                f"Calculator: `calculator_base_dir` is expected to be a str, not {type(value)}"
            )

    @property
    def base_dir(self):
        base_dir = Path(self.instrument_base_dir) / self.calculator_base_dir
        return str(base_dir)

    @property
    def output_file_paths(self):
        paths = []
        for filename in self.output_filenames:
            path = Path(self.base_dir) / filename
            # Make sure the file directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            paths.append(str(path))
        return paths

    @abstractmethod
    def backengine(self):
        Path(self.base_dir).mkdir(parents=True, exist_ok=True)
        input_num0 = self.input[self.input_keys[0]].get_data()["number"]
        input_num1 = self.input[self.input_keys[1]].get_data()["number"]
        output_num = float(input_num0) + float(input_num1)
        if self.parameters["plus_times"].value > 1:
            for i in range(self.parameters["plus_times"].value - 1):
                output_num += input_num1
        data_dict = {"number": output_num}
        key = self.output_keys[0]
        output_data = NumberData.from_dict(data_dict, key)
        self.output = DataCollection(output_data)
        return self.output
