import unittest
import os
import json
import numpy
from jsons import JsonSerializable

from pyvinyl.BaseCalculator import BaseCalculator, BaseParameters
from pyvinyl.BaseCalculator import SpecializedParameters, SpecializedCalculator
from pyvinyl.AbstractBaseClass import AbstractBaseClass

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

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

    def test_copy_construction(self):
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

        self.assertRaises(TypeError, SpecializedParameters)

        parameters = SpecializedParameters(
                photon_energy=10.0,
                pulse_energy=20.0,
                )

        self.assertIsInstance(parameters, SpecializedParameters)
        self.assertIsInstance(parameters, BaseParameters)
        self.assertIsInstance(parameters, JsonSerializable)
        self.assertIsInstance(parameters, AbstractBaseClass)

    def test_copy_construction(self):
        """ Test the copy constructor behaves as expected. """

        parameters = self.__default_parameters

        new_parameters = parameters(photon_energy=10.00)

        self.assertIsInstance(new_parameters, SpecializedParameters)
        self.assertIsInstance(new_parameters, BaseParameters)
        self.assertIsInstance(new_parameters, AbstractBaseClass)
        self.assertEqual(new_parameters.photon_energy, 10.00)
   
    def test_serialize_scalar(self):
        """ Test serialization of parameters. """
        # Test writing.
        parameters = self.__default_parameters

        # Test dumping to json dict.
        dump = parameters.dump()
        self.assertIsInstance(dump, dict)
        self.assertEqual(dump['photon_energy'], 109.98)
        self.assertEqual(dump['pulse_energy'], 32.39)
        
        # Test serialization to file.
        parameters.to_json("tmp_scalar.json")
        self.assertIn('tmp_scalar.json',
               os.listdir( os.path.abspath(os.path.dirname(__file__))))

        # Test loading.
        new_parameters = SpecializedParameters.from_json('tmp_scalar.json')
        self.assertIsInstance(new_parameters, SpecializedParameters)
        self.assertEqual(new_parameters.photon_energy, 109.98)
        self.assertEqual(dump['pulse_energy'], 32.39)

        # Update.
        new_parameters.pulse_energy = 763.43
        self.assertEqual(new_parameters.photon_energy, 109.98)
        self.assertEqual(new_parameters.pulse_energy, 763.43)

    def test_serialize_numpy(self):
        """ Test serialization of parameters. """
        # Test writing.
        photon_energy=numpy.linspace(10.0,100.0,100)
        photon_energy_norm = numpy.linalg.norm(photon_energy)

        pulse_energy=3.e-6
        parameters = SpecializedParameters(
                photon_energy=photon_energy,
                pulse_energy=pulse_energy,
                )

        # Test dumping to json dict.
        dump = parameters.dump()

        self.assertIsInstance(dump, dict)
        self.assertEqual(numpy.linalg.norm(dump['photon_energy']),
                photon_energy_norm)
        self.assertEqual(dump['pulse_energy'], pulse_energy)
        
        # Test serialization to file.
        fname='tmp_numpy.json'
        parameters.to_json(fname)
        self.assertIn(fname,
               os.listdir( os.path.abspath(os.path.dirname(__file__))))

        # Test loading.
        new_parameters = SpecializedParameters.from_json(fname)
        self.assertIsInstance(new_parameters, SpecializedParameters)
        self.assertEqual(numpy.linalg.norm(new_parameters.photon_energy),
                photon_energy_norm)
        self.assertEqual(dump['pulse_energy'], pulse_energy)

        # Update.
        new_parameters.pulse_energy = numpy.linspace(10.0,20.0,11)
        self.assertEqual(numpy.linalg.norm(new_parameters.photon_energy),
                photon_energy_norm)
        self.assertEqual(numpy.linalg.norm(new_parameters.pulse_energy),
                numpy.linalg.norm(numpy.linspace(10.0,20.0,11)))

    def test_serialize_object(self):
        """ Test serialization of parameters in the case of nested object
        parameters. """

        # Define nested parameters.
        class OuterParameters(BaseParameters):
            def __init__(self, 
                    inner_parameters:SpecializedParameters,
                    **kwargs,
                    ):

                super().__init__(
                        inner_parameters=inner_parameters,
                        **kwargs,
                        )

        
        inner = self.__default_parameters
        outer = OuterParameters(inner)

        outer_dump = outer.dump()


        self.assertIsInstance(outer_dump, dict)

        expected_dict = {'inner_parameters': {'photon_energy': 109.98, 'pulse_energy': 32.39}}
        self.assertEqual(
                outer_dump['inner_parameters']['photon_energy'],
                self.__default_parameters.photon_energy
                )
        self.assertEqual(
                outer_dump['inner_parameters']['pulse_energy'],
                self.__default_parameters.pulse_energy
                )


        # Test serialization to file.
        fname='tmp_nested.json'
        outer.to_json(fname)
        self.assertIn(fname,
               os.listdir( os.path.abspath(os.path.dirname(__file__))))

        # Test loading.
        new_parameters = OuterParameters.from_json(fname)
        self.assertIsInstance(new_parameters, OuterParameters)
        self.assertIsInstance(new_parameters.inner_parameters, SpecializedParameters        )
        

if __name__ == '__main__':
    unittest.main()

