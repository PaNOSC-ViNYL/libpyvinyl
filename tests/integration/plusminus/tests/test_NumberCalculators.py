#!/usr/bin/env python
"""Tests for `plusminus.NumberCalculators` package."""

import pytest
from plusminus.NumberCalculators import PlusCalculator, MinusCalculator
from plusminus.NumberData import NumberData, TXTFormat
from plusminus import DataCollection


def test_PlusCalculator():
    """PlusCalculator test function"""

    input1 = NumberData.from_dict({'number': 1}, 'input1')
    input2 = NumberData.from_dict({'number': 1}, 'input2')
    input_data = [input1, input2] # This could also be allowed.
    input_data = DataCollection(input1, input2)
    plus = PlusCalculator('plus', input_data)
    plus_output = plus.backengine()
    print(plus_output.get_data())
    plus_output.write('1_time.txt', TXTFormat)
    plus.parameters['plus_times'] = 5
    plus_output = plus.backengine()
    file_output = plus_output.write('5_time.txt', TXTFormat, key='file_output')
    print(file_output)

def test_MinusCalculator():
    """PlusCalculator test function"""

    input1 = NumberData.from_dict({'number': 1}, 'input1')
    input2 = NumberData.from_dict({'number': 1}, 'input2')
    input_data = DataCollection(input1, input2)
    plus = PlusCalculator('plus', input_data)
    plus_output = plus.backengine()
    print(plus_output.get_data())
    plus_output.write('1_time.txt', TXTFormat)
    plus.parameters['plus_times'] = 5
    plus_output = plus.backengine()
    file_output = plus_output.write('5_time.txt', TXTFormat, key='file_output')
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
