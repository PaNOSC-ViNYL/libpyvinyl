import unittest
import os
import shutil
import numpy
from jsons import JsonSerializable
import copy
import json

from SpecializedCalculator import SpecializedCalculator
from libpyvinyl.BaseCalculator import BaseCalculator
from libpyvinyl.Parameters import CalculatorParameters, InstrumentParameters
from libpyvinyl.AbstractBaseClass import AbstractBaseClass
from RandomImageCalculator import RandomImageCalculator

import logging

logging.basicConfig(format="%(asctime)s %(levelname)s:%(message)s", level=logging.DEBUG)


class BaseCalculatorTest(unittest.TestCase):
    """
    Test class for the BaseCalculator class.
    """

    @classmethod
    def setUpClass(cls):
        """Setting up the test class."""
        parameters = CalculatorParameters()
        photon_energy = parameters.new_parameter(
            "photon_energy", unit="keV", comment="Photon energy"
        )
        photon_energy.value = 109.98

        parameters.new_parameter("pulse_energy", unit="joule", comment="Pulse energy")
        parameters["pulse_energy"].value = 32.39
        cls.__default_parameters = parameters
        # cls.__default_parameters = SpecializedParameters(photon_energy=109.98,
        #                                                  pulse_energy=32.39)

        cls.__default_calculator = SpecializedCalculator(
            "default", cls.__default_parameters
        )

    @classmethod
    def tearDownClass(cls):
        """Tearing down the test class."""
        del cls.__default_parameters
        del cls.__default_calculator

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

        self.assertRaises(TypeError, BaseCalculator, self.__default_parameters)

    def test_default_construction(self):
        """Testing the default construction of the class."""

        # Test positional arguments
        # self.assertRaises(AttributeError, SpecializedCalculator)

        calculator = SpecializedCalculator("default", self.__default_parameters)

        self.assertIsInstance(calculator, SpecializedCalculator)
        self.assertIsInstance(calculator, BaseCalculator)
        self.assertIsInstance(calculator, AbstractBaseClass)

        self.assertRaises(TypeError, SpecializedCalculator, 1)

    def test_deep_copy(self):
        """Test the copy constructor behaves as expected."""

        new_parameters = copy.deepcopy(self.__default_parameters)
        new_parameters["photon_energy"].value = 10.00
        new_calculator = self.__default_calculator(parameters=new_parameters)
        self.assertIsInstance(new_calculator, SpecializedCalculator)
        self.assertIsInstance(new_calculator, BaseCalculator)
        self.assertIsInstance(new_calculator, AbstractBaseClass)
        self.assertEqual(new_calculator.parameters["photon_energy"].value, 10.00)

        new_parameters = copy.deepcopy(self.__default_parameters)
        new_parameters["pulse_energy"].value = 34.87
        new_calculator_2 = new_calculator(parameters=new_parameters)
        self.assertEqual(new_calculator_2.parameters["photon_energy"].value, 109.98)
        self.assertEqual(new_calculator_2.parameters["pulse_energy"].value, 34.87)

    def test_dump(self):
        """Test dumping to file."""
        calculator = self.__default_calculator

        self.__files_to_remove.append(calculator.dump())
        self.__files_to_remove.append(calculator.dump("dump.dill"))

    def test_resurrect_from_dump(self):
        """Test loading from dumpfile."""

        calculator = self.__default_calculator

        calculator.backengine()

        # dump
        dump = calculator.dump()
        self.__files_to_remove.append(dump)

        del calculator

        calculator = SpecializedCalculator("dump", dumpfile=dump)
        self.assertIsInstance(calculator, SpecializedCalculator)

        self.assertEqual(
            calculator.parameters["photon_energy"].value,
            self.__default_parameters["photon_energy"].value,
        )

        self.assertIsNotNone(calculator.data)

    def test_attributes(self):
        """Test that all required attributes are present."""

        calculator = self.__default_calculator

        self.assertTrue(hasattr(calculator, "parameters"))
        self.assertTrue(hasattr(calculator, "backengine"))
        self.assertTrue(hasattr(calculator, "_run"))
        self.assertTrue(hasattr(calculator, "saveH5"))
        self.assertTrue(hasattr(calculator, "data"))
        self.assertTrue(hasattr(SpecializedCalculator, "run_from_cli"))

    def test_derived_class(self):
        """Test that a derived class is functional."""
        parameters = CalculatorParameters()
        parameters.new_parameter("photon_energy", unit="eV", comment="Photon energy")
        parameters["photon_energy"].value = 6e3

        parameters.new_parameter("pulse_energy", unit="joule", comment="Pulse energy")
        parameters["pulse_energy"].value = 1.0e-6

        parameters.new_parameter("grid_size_x", unit="", comment="grid size x")
        parameters["grid_size_x"].value = 128
        parameters.new_parameter("grid_size_y", unit="", comment="grid size y")
        parameters["grid_size_y"].value = 128

        # Setup the calculator
        calculator = RandomImageCalculator("ramdom", parameters, output_path="out.h5")

        # Run the backengine
        self.assertEqual(calculator.backengine(), 0)

        # Look at the data and store as hdf5
        self.assertSequenceEqual(calculator.data.shape, (128, 128))

        # Save as h5.
        calculator.saveH5(calculator.output_path)
        self.assertIn(calculator.output_path, os.listdir())
        self.__files_to_remove.append(calculator.output_path)

        # Save the parameters to a human readable json file.
        parameters.to_json("my_parameters.json")
        self.assertIn("my_parameters.json", os.listdir())
        self.__files_to_remove.append("my_parameters.json")

        # Save calculator to binary dump.
        dumpfile = calculator.dump()
        self.__files_to_remove.append(dumpfile)
        self.assertIn(os.path.basename(dumpfile), os.listdir())

        # Load back parameters
        new_parameters = CalculatorParameters.from_json("my_parameters.json")
        self.assertEqual(
            new_parameters["photon_energy"].value,
            calculator.parameters["photon_energy"].value,
        )

        reloaded_calculator = SpecializedCalculator("derived", dumpfile=dumpfile)
        reloaded_calculator.data

        self.assertAlmostEqual(
            numpy.linalg.norm(reloaded_calculator.data - calculator.data), 0.0
        )

        reloaded_calculator.parameters["photon_energy"].value
        self.assertEqual(
            reloaded_calculator.parameters["photon_energy"].value,
            calculator.parameters["photon_energy"].value,
        )

    def test_set_values(self):
        calculator = self.__default_calculator

        calculator.set_parameters(photon_energy=42.0)
        self.assertEqual(calculator.parameters["photon_energy"].value, 42.0)

        calculator.set_parameters({"photon_energy": 37.0})
        self.assertEqual(calculator.parameters["photon_energy"].value, 37.0)


class ParametersTest(unittest.TestCase):
    """
    Test class for the BaseCalculator class.
    """

    @classmethod
    def setUpClass(cls):
        """Setting up the test class."""
        parameters = CalculatorParameters()
        parameters.new_parameter("photon_energy", unit="keV", comment="Photon energy")
        parameters["photon_energy"].value = 109.98

        parameters.new_parameter("pulse_energy", unit="joule", comment="Pulse energy")
        parameters["pulse_energy"].value = 32.39
        cls.__default_parameters = parameters
        # cls.__default_parameters = SpecializedParameters(photon_energy=109.98,
        #                                                  pulse_energy=32.39)

    @classmethod
    def tearDownClass(cls):
        """Tearing down the test class."""
        del cls.__default_parameters

    def setUp(self):
        """Setting up a test."""
        self.__files_to_remove = [
            "tmp_numpy.json",
            "tmp_scalar.json",
            "tmp_nested.json",
        ]
        self.__dirs_to_remove = []

    def tearDown(self):
        """Tearing down a test."""

        for f in self.__files_to_remove:
            if os.path.isfile(f):
                os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d):
                shutil.rmtree(d)

    def test_copy_construction(self):
        """Test the copy constructor behaves as expected."""

        new_parameters = copy.deepcopy(self.__default_parameters)

        new_parameters["photon_energy"].value = 10.00

        self.assertIsInstance(new_parameters, CalculatorParameters)
        self.assertIsInstance(new_parameters, AbstractBaseClass)
        self.assertEqual(new_parameters["photon_energy"].value, 10.00)
        self.assertEqual(
            new_parameters["pulse_energy"].value,
            self.__default_parameters["pulse_energy"].value,
        )

    def test_serialize_scalar(self):
        """Test serialization of parameters."""
        # Test writing.
        parameters = self.__default_parameters

        # Test dumping to json dict.
        dump = parameters.to_dict()
        self.assertIsInstance(dump, dict)
        self.assertEqual(dump["photon_energy"]["value"], 109.98)
        self.assertEqual(dump["pulse_energy"]["value"], 32.39)

        # Test serialization to file.
        parameters.to_json("tmp_scalar.json")
        self.assertIn(
            "tmp_scalar.json", os.listdir(os.path.abspath(os.path.dirname(__file__)))
        )

        # Test loading.
        new_parameters = CalculatorParameters.from_json("tmp_scalar.json")
        self.assertIsInstance(new_parameters, CalculatorParameters)
        self.assertEqual(new_parameters["photon_energy"].value, 109.98)
        self.assertEqual(dump["pulse_energy"]["value"], 32.39)

        # Update.
        new_parameters["pulse_energy"].value = 763.43
        self.assertEqual(new_parameters["photon_energy"].value, 109.98)
        self.assertEqual(new_parameters["pulse_energy"].value, 763.43)

    def test_serialize_list(self):
        """Test serialization of parameters."""

        # Define  parameters with numpy array as an argument.

        # Test writing.
        par = [i * 0.2354 for i in range(10)]
        sc = numpy.random.random()

        parameters = CalculatorParameters()
        parameters.new_parameter("array_par")
        parameters["array_par"].value = par
        parameters.new_parameter("scalar_par")
        parameters["scalar_par"].value = sc

        # Test dumping to json dict.
        dump = parameters.to_dict()

        self.assertIsInstance(dump, dict)
        self.assertSequenceEqual(dump["array_par"]["value"], par)
        self.assertEqual(dump["scalar_par"]["value"], sc)

        # Test serialization to file.
        fname = "tmp_numpy.json"
        parameters.to_json(fname)
        self.assertIn(fname, os.listdir(os.path.abspath(os.path.dirname(__file__))))

        # Test loading.
        new_parameters = CalculatorParameters.from_json(fname)
        self.assertIsInstance(new_parameters, CalculatorParameters)
        self.assertIsInstance(new_parameters["array_par"].value, list)
        self.assertSequenceEqual(new_parameters["array_par"].value, par)
        self.assertEqual(new_parameters["scalar_par"].value, sc)

    def test_serialize_object(self):
        """Test serialization of parameters in the case of nested object
        parameters."""

        # Define nested parameters.
        outer = InstrumentParameters()
        outer.add("inner_parameters", self.__default_parameters)

        outer_dump = outer.to_dict()
        # print(json.dumps(outer_dump, indent=4))

        self.assertIsInstance(outer_dump, dict)

        expected_dict = {
            "inner_parameters": {
                "photon_energy": {
                    "name": "photon_energy",
                    "unit": "keV",
                    "comment": "Photon energy",
                    "value": 109.98,
                    "legal_intervals": [],
                    "illegal_intervals": [],
                    "options": [],
                },
                "pulse_energy": {
                    "name": "pulse_energy",
                    "unit": "joule",
                    "comment": "Pulse energy",
                    "value": 32.39,
                    "legal_intervals": [],
                    "illegal_intervals": [],
                    "options": [],
                },
            }
        }

        self.assertEqual(
            outer_dump["inner_parameters"]["photon_energy"]["value"],
            self.__default_parameters["photon_energy"].value,
        )
        self.assertEqual(
            outer_dump["inner_parameters"]["pulse_energy"]["value"],
            self.__default_parameters["pulse_energy"].value,
        )

        # Test serialization to file.
        fname = "tmp_nested.json"
        outer.to_json(fname)
        self.assertIn(fname, os.listdir(os.path.abspath(os.path.dirname(__file__))))

        # Test loading.
        new_parameters = InstrumentParameters.from_json(fname)
        self.assertIsInstance(new_parameters, InstrumentParameters)
        self.assertIsInstance(new_parameters["inner_parameters"], CalculatorParameters)


if __name__ == "__main__":
    unittest.main()
