#!/usr/bin/env python
"""Tests for `plusminus.NumberCalculators` package."""

import pytest
from plusminus.ArrayCalculators import ArrayCalculator
from plusminus.NumberData import NumberData
from plusminus.ArrayData import TXTFormat
from plusminus import DataCollection


def test_ArrayCalculator(tmpdir):
    """PlusCalculator test function, the native output of ArrayCalculator is a python dictionary"""

    input1 = NumberData.from_dict({"number": 1}, "input1")
    input2 = NumberData.from_dict({"number": 2}, "input2")
    input_data = [input1, input2]  # This could also be allowed.
    input_data = DataCollection(input1, input2)
    calculator = ArrayCalculator("plus", input_data)
    calculator.set_instrument_base_dir(str(tmpdir))
    output = calculator.backengine()
    assert output.get_data()["array"][0] == 1
    assert output.get_data()["array"][1] == 2
    calculator.parameters["multiply"] = 5
    output = calculator.backengine()
    file_output = output.write(
        calculator.base_dir + "/array_5.txt", TXTFormat, key="file_output"
    )
    assert file_output.get_data()["array"][0] == 5
    assert file_output.get_data()["array"][1] == 10
