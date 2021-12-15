from typing import Union
from pathlib import Path
import numpy as np
from libpyvinyl import CalculatorParameters
from libpyvinyl.BaseData import DataCollection
from plusminus.BaseCalculator import BaseCalculator
from plusminus.NumberData import NumberData
from plusminus.ArrayData import ArrayData


class ArrayCalculator(BaseCalculator):
    def __init__(self,
                 name: str,
                 input: Union[DataCollection, list, NumberData],
                 output_keys: Union[list, str] = ['array_result'],
                 output_data_types=[ArrayData],
                 output_filenames=[],
                 instrument_base_dir='./',
                 calculator_base_dir='ArrayCalculator',
                 parameters: CalculatorParameters = None):
        """A python dict calculator to create an array from two inputs."""
        super().__init__(name,
                         input,
                         output_keys,
                         output_data_types=output_data_types,
                         output_filenames=output_filenames,
                         instrument_base_dir=instrument_base_dir,
                         calculator_base_dir=calculator_base_dir,
                         parameters=parameters)

    def init_parameters(self):
        parameters = CalculatorParameters()
        # Calculator developer edit
        multiply = parameters.new_parameter(
            "multiply", comment="Multiply the array by a value")
        multiply.value = 1
        # Calculator developer end
        self.parameters = parameters

    def backengine(self):
        Path(self.base_dir).mkdir(parents=True, exist_ok=True)
        input_data0 = self.input.to_list()[0]
        assert type(input_data0) is NumberData
        input_num0 = input_data0.get_data()['number']
        input_data1 = self.input.to_list()[1]
        assert type(input_data1) is NumberData
        input_num1 = input_data1.get_data()['number']
        output_arr = np.array([input_num0, input_num1
                               ]) * self.parameters['multiply'].value
        data_dict = {'array': output_arr}
        key = self.output_keys[0]
        output_data = ArrayData.from_dict(data_dict, key)
        self.output = DataCollection(output_data)
        return self.output
