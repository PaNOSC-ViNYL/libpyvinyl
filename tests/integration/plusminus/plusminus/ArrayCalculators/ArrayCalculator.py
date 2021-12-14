from pathlib import Path
import numpy as np
from libpyvinyl import BaseCalculator, CalculatorParameters
from libpyvinyl.BaseData import DataCollection
from plusminus.NumberData import NumberData
from plusminus.ArrayData import ArrayData


class ArrayCalculator(BaseCalculator):
    def __init__(self,
                 name: str,
                 input: DataCollection,
                 input_keys=['input1', 'input2'],
                 output_keys=['array_result'],
                 output_filenames=[],
                 parameters=None):
        """A python dict calculator to create an array from two inputs."""
        if parameters is None:
            self.__init_parameters()
        self.__name = name
        self.__input = input
        assert len(input_keys) == 2
        self.__input_keys = input_keys
        self.__base_dir = None
        self.base_dir = 'ArrayCalculator'
        assert len(output_keys) == 1
        self.__output_keys = output_keys
        assert len(output_filenames) == 0
        self.__output_filenames = output_filenames

    def __init_parameters(self):
        parameters = CalculatorParameters()
        multiply = parameters.new_parameter(
            "multiply", comment="Multiply the array by a value")
        multiply.value = 1
        self.parameters = parameters

    @property
    def name(self):
        return self.__name

    @property
    def input(self):
        return self.__input

    @property
    def base_dir(self):
        return self.__base_dir

    @base_dir.setter
    def base_dir(self, value):
        self.set_base_dir(value)

    def set_base_dir(self, value):
        # Make sure the base_dir exists and set the base_dir.
        Path(value).mkdir(parents=True, exist_ok=True)
        self.__base_dir = value

    @property
    def input_keys(self):
        return self.__input_keys

    @property
    def output_keys(self):
        return self.__output_keys

    @property
    def output_filenames(self):
        """Native calculator file names"""
        return self.__output_filenames

    @output_filenames.setter
    def output_filenames(self, value):
        self.set_output_filenames(value)

    def set_output_filenames(self, value):
        if isinstance(value, str):
            self.__output_filenames = [value]
        else:
            self.__output_filenames = value

    @property
    def output_file_paths(self):
        paths = []
        for filename in self.output_filenames:
            path = Path(self.base_dir) / filename
            # Make sure the file directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            paths.append(str(path))
        return paths

    def backengine(self):
        input_data0 = self.input[self.input_keys[0]]
        assert type(input_data0) is NumberData
        input_num0 = input_data0.get_data()['number']
        input_data1 = self.input[self.input_keys[1]]
        assert type(input_data1) is NumberData
        input_num1 = input_data1.get_data()['number']
        output_arr = np.array([input_num0, input_num1
                               ]) * self.parameters['multiply'].value
        data_dict = {'array': output_arr}
        key = self.output_keys[0]
        output_data = ArrayData.from_dict(data_dict, key)
        self.output = DataCollection(output_data)
        return self.output

    def saveH5(self, fname: str, openpmd: bool = True):
        raise NotImplementedError
