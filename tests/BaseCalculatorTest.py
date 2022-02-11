import unittest
import pytest
import os
import shutil
from typing import Union
from pathlib import Path

from libpyvinyl.BaseCalculator import BaseCalculator
from libpyvinyl.BaseData import BaseData, DataCollection
from libpyvinyl.Parameters import CalculatorParameters
from libpyvinyl.AbstractBaseClass import AbstractBaseClass

import logging

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)


class NumberData(BaseData):
    """Example dict mapping data"""

    def __init__(
        self,
        key,
        data_dict=None,
        filename=None,
        file_format_class=None,
        file_format_kwargs=None,
    ):

        expected_data = {}

        ### DataClass developer's job start
        expected_data["number"] = None
        ### DataClass developer's job end

        super().__init__(
            key,
            expected_data,
            data_dict,
            filename,
            file_format_class,
            file_format_kwargs,
        )

    @classmethod
    def supported_formats(self):
        return {}

    @classmethod
    def from_file(cls, filename: str, format_class, key, **kwargs):
        raise NotImplementedError()

    @classmethod
    def from_dict(cls, data_dict, key):
        """Create the data class by a python dictionary."""
        return cls(key, data_dict=data_dict)


class PlusCalculator(BaseCalculator):
    def __init__(
        self,
        name: str,
        input: Union[DataCollection, list, NumberData],
        output_keys: Union[list, str] = ["plus_result"],
        output_data_types=[NumberData],
        output_filenames: Union[list, str] = [],
        instrument_base_dir="./",
        calculator_base_dir="PlusCalculator",
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
            "plus_times", comment="How many times to do the plus"
        )
        # Set defaults
        times.value = 1

        self.parameters = parameters

    def backengine(self):
        Path(self.base_dir).mkdir(parents=True, exist_ok=True)
        input_num0 = self.input.to_list()[0].get_data()["number"]
        input_num1 = self.input.to_list()[1].get_data()["number"]
        output_num = float(input_num0) + float(input_num1)
        if self.parameters["plus_times"].value > 1:
            for i in range(self.parameters["plus_times"].value - 1):
                output_num += input_num1
        data_dict = {"number": output_num}
        key = self.output_keys[0]
        output_data = self.output[key]
        output_data.set_dict(data_dict)
        return self.output


class BaseCalculatorTest(unittest.TestCase):
    """
    Test class for the BaseCalculator class.
    """

    @classmethod
    def setUpClass(cls):
        """Setting up the test class."""

        input1 = NumberData.from_dict({"number": 1}, "input1")
        input2 = NumberData.from_dict({"number": 1}, "input2")
        input_data = [input1, input2]
        plus = PlusCalculator("plus", input_data)
        cls.__default_calculator = plus
        cls.__default_input = input_data

    @classmethod
    def tearDownClass(cls):
        """Tearing down the test class."""
        del cls.__default_calculator
        del cls.__default_input

    def setUp(self):
        """Setting up a test."""
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """Tearing down a test."""

        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def test_base_class_constructor_raises(self):
        """Test that we cannot construct instances of the base class."""

        self.assertRaises(TypeError, BaseCalculator, "name")

    def test_default_construction(self):
        """Testing the default construction of the class."""

        # Test positional arguments
        calculator = PlusCalculator("test", self.__default_input)

        self.assertIsInstance(calculator, PlusCalculator)
        self.assertIsInstance(calculator, BaseCalculator)
        self.assertIsInstance(calculator, AbstractBaseClass)

    def test_deep_copy(self):
        """Test the copy constructor behaves as expected."""
        # Parameters are not deepcopied by itself
        calculator_copy = self.__default_calculator()
        self.assertEqual(calculator_copy.parameters["plus_times"].value, 1)
        new_parameters = calculator_copy.parameters
        new_parameters["plus_times"] = 5
        self.assertEqual(new_parameters["plus_times"].value, 5)
        self.assertEqual(calculator_copy.parameters["plus_times"].value, 5)

        # Parameters are deepcopied when copy the calculator
        calculator_copy = self.__default_calculator()
        self.assertEqual(calculator_copy.parameters["plus_times"].value, 1)
        calculator_copy.parameters["plus_times"] = 10
        self.assertEqual(calculator_copy.parameters["plus_times"].value, 10)
        self.assertEqual(self.__default_calculator.parameters["plus_times"].value, 1)
        calculator_copy.input["input1"] = NumberData.from_dict({"number": 5}, "input1")
        self.assertEqual(calculator_copy.input["input1"].get_data()["number"], 5)
        self.assertEqual(
            self.__default_calculator.input["input1"].get_data()["number"], 1
        )

        # Calculator reference
        self.assertEqual(calculator_copy.parameters["plus_times"].value, 10)
        calculator_reference = calculator_copy
        self.assertEqual(calculator_reference.parameters["plus_times"].value, 10)
        calculator_reference.parameters["plus_times"] = 3
        self.assertEqual(calculator_reference.parameters["plus_times"].value, 3)
        self.assertEqual(calculator_copy.parameters["plus_times"].value, 3)

        # New parameters can be set while caculator deepcopy
        new_parameters = CalculatorParameters()
        times = new_parameters.new_parameter(
            "plus_times", comment="How many times to do the plus"
        )
        times.value = 1
        new_parameters["plus_times"].value = 5
        new_calculator = self.__default_calculator(parameters=new_parameters)
        self.assertIsInstance(new_calculator, PlusCalculator)
        self.assertIsInstance(new_calculator, BaseCalculator)
        self.assertIsInstance(new_calculator, AbstractBaseClass)
        self.assertEqual(new_calculator.parameters["plus_times"].value, 5)
        self.assertEqual(self.__default_calculator.parameters["plus_times"].value, 1)

    def test_dump(self):
        """Test dumping to file."""
        calculator = self.__default_calculator

        self.__files_to_remove.append(calculator.dump())
        self.__files_to_remove.append(calculator.dump("dump.dill"))

    def test_parameters_in_copied_calculator(self):
        """Test parameters in a copied calculator"""

        calculator = self.__default_calculator
        self.assertEqual(calculator.parameters["plus_times"].value, 1)
        calculator.parameters["plus_times"] = 5
        self.assertEqual(self.__default_calculator.parameters["plus_times"].value, 5)
        calculator.parameters["plus_times"] = 1
        self.assertEqual(self.__default_calculator.parameters["plus_times"].value, 1)

    def test_resurrect_from_dump(self):
        """Test loading from dumpfile."""

        calculator = self.__default_calculator()

        self.assertEqual(calculator.parameters["plus_times"].value, 1)
        output = calculator.backengine()
        self.assertEqual(output.get_data()["number"], 2)
        self.__dirs_to_remove.append("PlusCalculator")

        # dump
        dump = calculator.dump()
        self.__files_to_remove.append(dump)

        del calculator

        calculator = PlusCalculator.from_dump(dump)

        self.assertEqual(
            calculator.input.get_data(),
            self.__default_calculator.input.get_data(),
        )

        calculator.parameters.to_dict()
        self.assertEqual(
            calculator.parameters.to_dict(),
            self.__default_calculator.parameters.to_dict(),
        )

        calculator.parameters["plus_times"] = 5
        self.assertNotEqual(
            calculator.parameters.to_dict(),
            self.__default_calculator.parameters.to_dict(),
        )

        self.assertIsNotNone(calculator.data)

    def test_attributes(self):
        """Test that all required attributes are present."""

        calculator = self.__default_calculator

        self.assertTrue(hasattr(calculator, "name"))
        self.assertTrue(hasattr(calculator, "input"))
        self.assertTrue(hasattr(calculator, "output"))
        self.assertTrue(hasattr(calculator, "parameters"))
        self.assertTrue(hasattr(calculator, "instrument_base_dir"))
        self.assertTrue(hasattr(calculator, "calculator_base_dir"))
        self.assertTrue(hasattr(calculator, "base_dir"))
        self.assertTrue(hasattr(calculator, "backengine"))
        self.assertTrue(hasattr(calculator, "data"))
        self.assertTrue(hasattr(calculator, "dump"))
        self.assertTrue(hasattr(calculator, "from_dump"))

    def test_set_param_values(self):
        calculator = self.__default_calculator

        calculator.parameters["plus_times"] = 5
        self.assertEqual(calculator.parameters["plus_times"].value, 5)

    def test_collection_get_data(self):
        calculator = self.__default_calculator
        print(calculator.input)
        input_dict = calculator.input.get_data()
        self.assertEqual(input_dict["input1"]["number"], 1)
        self.assertEqual(input_dict["input2"]["number"], 1)

    def test_output_file_paths(self):
        calculator = self.__default_calculator
        with self.assertRaises(ValueError):
            calculator.output_file_paths
        calculator.output_filenames = "bingo.txt"
        self.assertEqual(calculator.output_file_paths[0], "PlusCalculator/bingo.txt")
        self.__dirs_to_remove.append("PlusCalculator")


if __name__ == "__main__":
    unittest.main()
