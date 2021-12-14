from typing import Union
from libpyvinyl import CalculatorParameters
from libpyvinyl.BaseData import DataCollection
from plusminus.NumberData import NumberData
from plusminus.BaseCalculator import BaseCalculator


class PlusCalculator(BaseCalculator):
    def __init__(self,
                 name: str,
                 input: Union[DataCollection, list, NumberData],
                 input_keys: Union[list, str] = ['input1', 'input2'],
                 output_keys: Union[list, str] = ['plus_result'],
                 output_data_types=[NumberData],
                 output_filenames: Union[list, str] = [],
                 instrument_base_dir='./',
                 calculator_base_dir='PlusCalculator',
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
            "plus_times", comment="How many times to do the plus")
        times.value = 1
        self.parameters = parameters

    def backengine(self):
        input_num0 = self.input[self.input_keys[0]].get_data()['number']
        input_num1 = self.input[self.input_keys[1]].get_data()['number']
        output_num = float(input_num0) + float(input_num1)
        if self.parameters['plus_times'].value > 1:
            for i in range(self.parameters['plus_times'].value - 1):
                output_num += input_num1
        data_dict = {'number': output_num}
        key = self.output_keys[0]
        output_data = self.output[key]
        output_data.set_dict(data_dict, key)
        return self.output
