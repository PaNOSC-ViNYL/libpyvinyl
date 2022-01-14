#!/usr/bin/env python
"""Tests for `plusminus.NumberCalculators` package."""

import pytest
from plusminus.NumberCalculators import PlusCalculator, MinusCalculator
from plusminus.NumberData import NumberData, TXTFormat
from plusminus import DataCollection


def test_PlusCalculator(tmpdir):
    """PlusCalculator test function, the native output of PlusCalculator is a python dictionary"""

    input1 = NumberData.from_dict({"number": 1}, "input1")
    input2 = NumberData.from_dict({"number": 1}, "input2")
    input_data = [input1, input2]  # This could also be allowed.
    input_data = DataCollection(input1, input2)
    plus = PlusCalculator("plus", input_data)
    plus.set_instrument_base_dir(str(tmpdir))
    plus_output = plus.backengine()
    assert plus_output.get_data()["number"] == 2
    plus_output.write(plus.base_dir + "/1_time.txt", TXTFormat)
    plus.parameters["plus_times"] = 5
    plus_output = plus.backengine()
    file_output = plus_output.write(
        plus.base_dir + "/5_time.txt", TXTFormat, key="file_output"
    )
    assert file_output.get_data()["number"] == 6


def test_MinusCalculator(tmpdir):
    """MinusCalculator test function. The native output of MinusCalculator is a txt file"""

    input1 = NumberData.from_dict({"number": 1}, "input1")
    input2 = NumberData.from_dict({"number": 1}, "input2")
    input_data = DataCollection(input1, input2)
    calculator = MinusCalculator("minus", input_data)
    calculator.set_instrument_base_dir(str(tmpdir))
    assert "MinusCalculator" in calculator.base_dir
    calculator.set_output_filenames("minus_res.txt")
    output = calculator.backengine()
    assert output.get_data()["number"] == 0
    calculator.parameters["minus_times"] = 5
    plus_output = calculator.backengine()
    assert plus_output.get_data()["number"] == -4


def test_DataCollection_multiple():
    """PlusCalculator test function"""

    input1 = NumberData.from_dict({"number": 1}, "input1")
    input2 = NumberData.from_dict({"number": 1}, "input2")
    input_data = DataCollection(input1, input2)
    data = input_data.get_data()
    assert data["input1"]["number"] == 1
    assert data["input2"]["number"] == 1
