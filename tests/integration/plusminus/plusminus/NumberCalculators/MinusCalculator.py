from typing import Union
import numpy as np
from libpyvinyl import CalculatorParameters
from libpyvinyl.BaseData import DataCollection
from plusminus.NumberData import NumberData, TXTFormat
from plusminus.BaseCalculator import BaseCalculator


class MinusCalculator(BaseCalculator):
    def __init__(self,
                 name: str,
                 input: Union[DataCollection, list, NumberData],
                 input_keys: Union[list, str] = ['input1', 'input2'],
                 output_keys: Union[list, str] = ['minus_result'],
                 output_data_types=[NumberData],
                 output_filenames: Union[list, str] = ['minus_result.txt'],
                 instrument_base_dir='./',
                 calculator_base_dir='MinusCalculator',
                 parameters=None):
        """A python object calculator example"""
        super().__init__(name,
                         input,
                         input_keys,
                         output_keys,
                         output_data_types=output_data_types,
                         output_filenames=output_filenames,
                         instrument_base_dir=instrument_base_dir,
                         calculator_base_dir=calculator_base_dir,
                         parameters=parameters)

    def init_parameters(self):
        parameters = CalculatorParameters()
        times = parameters.new_parameter(
            "minus_times", comment="How many times to do the minus")
        times.value = 1
        self.parameters = parameters

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
