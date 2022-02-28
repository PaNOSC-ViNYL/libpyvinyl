from typing import Union
from pathlib import Path
import numpy as np
from libpyvinyl.BaseData import DataCollection
from plusminus.NumberData import NumberData, TXTFormat
from libpyvinyl.BaseCalculator import BaseCalculator, CalculatorParameters


class MinusCalculator(BaseCalculator):
    def __init__(
        self,
        name: str,
        input: Union[DataCollection, list, NumberData],
        output_keys: Union[list, str] = ["minus_result"],
        output_data_types=[NumberData],
        output_filenames: Union[list, str] = ["minus_result.txt"],
        instrument_base_dir="./",
        calculator_base_dir="MinusCalculator",
        parameters=None,
    ):
        """A python object calculator example"""
        super().__init__(
            name,
            input,
            output_keys,
            output_data_types=output_data_types,
            output_filenames=output_filenames,
            instrument_base_dir=instrument_base_dir,
            calculator_base_dir=calculator_base_dir,
            parameters=parameters,
        )

    def init_parameters(self):
        parameters = CalculatorParameters()
        times = parameters.new_parameter(
            "minus_times", comment="How many times to do the minus"
        )
        times.value = 1
        self.parameters = parameters

    def backengine(self):
        Path(self.base_dir).mkdir(parents=True, exist_ok=True)
        input_num0 = self.input.to_list()[0].get_data()["number"]
        input_num1 = self.input.to_list()[1].get_data()["number"]
        output_num = float(input_num0) - float(input_num1)
        if self.parameters["minus_times"].value > 1:
            for i in range(self.parameters["minus_times"].value - 1):
                output_num -= input_num1
        arr = np.array([output_num])
        file_path = self.output_file_paths[0]
        np.savetxt(file_path, arr, fmt="%.3f")
        key = self.output_keys[0]
        output_data = self.output[key]
        output_data.set_file(file_path, TXTFormat)
        return self.output
