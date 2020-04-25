import unittest
import os

from pyvinyl.BaseCalculator import BaseCalculator, BaseParameters
from pyvinyl.BaseCalculator import SpecializedParameters, SpecializedCalculator
from pyvinyl.AbstractBaseClass import AbstractBaseClass


class BaseCalculatorTest(unittest.TestCase):
    """
    Test class for the BaseCalculator class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.__default_parameters = SpecializedParameters(photon_energy=109.98,
                pulse_energy=32.39)
        cls.__default_calculator = SpecializedCalculator(cls.__default_parameters)

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        del cls.__default_parameters
        del cls.__default_calculator

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """

        for f in self.__files_to_remove:
            if os.path.isfile(f): os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d): shutil.rmtree(d)

    def test_base_class_constructor_raises(self):
        """ Test that we cannot construct instances of the base class. """

        self.assertRaises(TypeError, BaseCalculator, self.__default_parameters)

    def test_default_construction(self):
        """ Testing the default construction of the class. """

        # Test positional arguments
        self.assertRaises(AttributeError, SpecializedCalculator)

        calculator = SpecializedCalculator(self.__default_parameters)

        self.assertIsInstance(calculator, SpecializedCalculator)
        self.assertIsInstance(calculator, BaseCalculator)
        self.assertIsInstance(calculator, AbstractBaseClass)

        self.assertRaises(TypeError, SpecializedCalculator, 1)

    def test_dump(self):
        """ Test dumping to file. """
        calculator = self.__default_calculator
        
        self.__files_to_remove.append(calculator.dump())
        self.__files_to_remove.append(calculator.dump("dump.dill"))
    
    def test_resurrect_from_dump(self):
        """ Test loading from dumpfile. """
        calculator = self.__default_calculator

        # dump
        dump = calculator.dump()
        self.__files_to_remove.append(dump)

        del calculator

        calculator = SpecializedCalculator(dumpfile=dump)
        self.assertIsInstance(calculator, SpecializedCalculator)

        self.assertEqual(calculator.parameters.photon_energy,
                self.__default_parameters.photon_energy)


class BaseParametersTest(unittest.TestCase):
    """
    Test class for the BaseCalculator class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        cls.__default_parameters = SpecializedParameters(photon_energy=109.98,
                pulse_energy=32.39)

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        del cls.__default_parameters

    def setUp(self):
        """ Setting up a test. """
        self.__files_to_remove = []
        self.__dirs_to_remove = []

    def tearDown(self):
        """ Tearing down a test. """

        for f in self.__files_to_remove:
            if os.path.isfile(f): os.remove(f)
        for d in self.__dirs_to_remove:
            if os.path.isdir(d): shutil.rmtree(d)

    def test_base_class_constructor_raises(self):
        """ Test that we cannot construct instances of the base class. """

        self.assertRaises(TypeError, BaseParameters)

    def test_default_construction(self):
        """ Testing the default construction of the class. """

        # Test positional arguments
        self.assertRaises(TypeError, SpecializedCalculator)

        parameters = SpecializedParameters()
        self.assertIsInstance(parameters, SpecializedParameters)
        self.assertIsInstance(parameters, BaseParameters)
        self.assertIsInstance(parameters, AbstractBaseClass)

    def test_copy_construction(self):
        """ Test the copy constructor behaves as expected. """

        parameters = self.__default_parameters

        new_parameters = parameters(photon_energy=10.00)

        self.assertIsInstance(new_parameters, SpecializedParameters)
        self.assertIsInstance(new_parameters, BaseParameters)
        self.assertIsInstance(new_parameters, AbstractBaseClass)
        self.assertEqual(new_parameters.photon_energy, 10.00)

    def test_copy_construct_calculator(self):
        """ Test the copy constructor behaves as expected. """

        new_parameters = self.__default_parameters(photon_energy=10.00)
        new_calculator = self.__default_calculator(parameters=new_parameters)
        self.assertIsInstance(new_calculator, SpecializedCalculator)
        self.assertIsInstance(new_calculator, BaseCalculator)
        self.assertIsInstance(new_calculator, AbstractBaseClass)
        self.assertEqual(new_calculator.parameters.photon_energy, 10.00)

        new_calculator_2 = new_calculator(parameters=self.__default_parameters(pulse_energy=34.87))
        self.assertEqual(new_calculator_2.parameters.photon_energy, 109.98)
        self.assertEqual(new_calculator_2.parameters.pulse_energy, 34.87)
    
    def test_serialize(self):
        """ Test serialization of parameters. """
        self.assertFalse(True)

    def test_unserialize(self):
        """ Test loading of parameters from serialized. """
        self.assertFalse(True)
    

if __name__ == '__main__':
    unittest.main()

