from pathlib import Path
import numpy as np
from libpyvinyl import BaseCalculator, CalculatorParameters
from libpyvinyl.BaseData import DataCollection
from plusminus.NumberData import NumberData, TXTFormat


class MinusCalculator(BaseCalculator):
    def __init__(self,
                 name: str,
                 input: DataCollection,
                 input_keys=['input1', 'input2'],
                 output_keys=['mius_result'],
                 output_filenames=['minus_result.txt'],
                 parameters=None):
        """A file calculator example."""
        if parameters is None:
            self.__init_parameters()
        self.__name = name
        self.__input = input
        assert len(input_keys) == 2
        self.__input_keys = input_keys
        self.__base_dir = None
        self.base_dir = 'MinusCalculator'
        assert len(output_keys) == 1
        self.__output_keys = output_keys
        assert len(output_filenames) == 1
        self.__output_filenames = output_filenames
        self.__init_output()

    def __init_output(self):
        output = DataCollection()
        for key in self.output_keys:
            output_data = NumberData(key)
            output.add_data(output_data)
        self.output = output

    def __init_parameters(self):
        parameters = CalculatorParameters()
        times = parameters.new_parameter(
            "minus_times", comment="How many times to do the minus")
        times.value = 1
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
        input_num0 = self.input[self.input_keys[0]].get_data()['number']
        input_num1 = self.input[self.input_keys[1]].get_data()['number']
        output_num = float(input_num0) - float(input_num1)
        if self.parameters['minus_times'].value > 1:
            for i in range(self.parameters['minus_times'].value - 1):
                output_num -= input_num1
        arr = np.array([output_num])
        file_path = self.output_file_paths[0]
        np.savetxt(file_path, arr, fmt='%.3f')
        key = self.output_keys[0]
        output_data = self.output[key]
        output_data.set_file(file_path, TXTFormat, key)
        return self.output

    def saveH5(self, fname: str, openpmd: bool = True):
        raise NotImplementedError
