import os
import numpy as np
from libpyvinyl import BaseCalculator, CalculatorParameters
from libpyvinyl.BaseData import DataCollection
from plusminus.NumberData import NumberData, TXTFormat


class MinusCalculator(BaseCalculator):
    def __init__(self,
                 name: str,
                 input: DataCollection,
                 output_keys=['mius_result'],
                 output_filenames=['minus_result.txt'],
                 parameters=None):
        """A file calculator example."""
        if parameters is None:
            self.__init_parameters()
        self.__name = name
        self.__input = input
        self.__request_data_source_keys = ['number1', 'number2']
        self.__base_dir = './'
        self.__output_keys = output_keys
        self.__output_filenames = output_filenames

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
        self.__base_dir = value

    @property
    def output_keys(self):
        return self.__output_keys

    @property
    def output_filenames(self):
        """Native calculator file names"""
        return self.__output_filenames

    @property
    def output_file_paths(self):
        paths = []
        for filename in self.output_filenames:
            path = os.path.join(self.base_dir, filename)
            paths.append(path)
        return paths

    @property
    def request_data_keys(self):
        return self.__request_data_source_keys

    def backengine(self):
        input_num0 = input[self.request_data_keys[0]].get_data()['number']
        input_num1 = input[self.request_data_keys[1]].get_data()['number']
        output_num = input_num0 - input_num1
        arr = np.array([output_num])
        filename = self.output_filenames[0]
        np.savetxt(filename, arr, fmt='%.3f')
        output_data = NumberData.from_file(filename, TXTFormat)
        self.output = DataCollection(output_data)
        return self.output
