#!/usr/bin/env python
"""Tests for `plusminus.NumberCalculators` package."""

import pytest
from plusminus.NumberCalculators import PlusCalculator, MinusCalculator
from plusminus.NumberData import NumberData, TXTFormat
from plusminus import DataCollection


def test_PlusCalculator():
    """PlusCalculator test function, the native output of MinusCalculator is a python dictionary"""

    input1 = NumberData.from_dict({'number': 1}, 'input1')
    input2 = NumberData.from_dict({'number': 1}, 'input2')
    input_data = [input1, input2]  # This could also be allowed.
    input_data = DataCollection(input1, input2)
    plus = PlusCalculator('plus', input_data)
    plus_output = plus.backengine()
    print(plus_output.get_data())
    plus_output.write(plus.base_dir + '/1_time.txt', TXTFormat)
    plus.parameters['plus_times'] = 5
    plus_output = plus.backengine()
    file_output = plus_output.write(plus.base_dir + '/5_time.txt',
                                    TXTFormat,
                                    key='file_output')
    print(file_output)


def test_MinusCalculator():
    """MinusCalculator test function. The native output of MinusCalculator is a txt file"""

    input1 = NumberData.from_dict({'number': 1}, 'input1')
    input2 = NumberData.from_dict({'number': 1}, 'input2')
    input_data = DataCollection(input1, input2)
    calculator = MinusCalculator('minus', input_data)
    print(calculator.base_dir)
    calculator.set_output_filenames('minus_res.txt')
    output = calculator.backengine()
    print(output.get_data())
    output.write(calculator.base_dir + '/1_time_minus.txt', TXTFormat)
    calculator.parameters['minus_times'] = 5
    plus_output = calculator.backengine()
    file_output = plus_output.write(calculator.base_dir + '/5_time_minus.txt',
                                    TXTFormat,
                                    key='file_output')
    print(file_output)


# def test_Instrument():


def test_DataCollection_multiple():
    """PlusCalculator test function"""

    input1 = NumberData.from_dict({'number': 1}, 'input1')
    input2 = NumberData.from_dict({'number': 1}, 'input2')
    input_data = DataCollection(input1, input2)
    with pytest.raises(RuntimeError) as excinfo:
        input_data.get_data()
        assert "More than 1 data object in this DataCollection" in str(
            excinfo.value)
