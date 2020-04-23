import unittest

from pyvinyl.BaseCalculator import BaseCalculator, BaseParameters
from pyvinyl.AbstractBaseClass import AbstractBaseClass


class BaseCalculatorTest(unittest.TestCase):
    """
    Test class for the BaseCalculator class.
    """

    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        pass

    @classmethod
    def tearDownClass(cls):
        """ Tearing down the test class. """
        pass

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

    def test_default_construction(self):
        """ Testing the default construction of the class. """

        # Test positional arguments
        self.assertRaises(TypeError, BaseCalculator)

        parameters = BaseParameters()
        self.assertIsInstance(parameters, BaseParameters)
        self.assertIsInstance(parameters, AbstractBaseClass)

        calculator = BaseCalculator(parameters)

        self.assertIsInstance(calculator, BaseCalculator)
        self.assertIsInstance(calculator, AbstractBaseClass)

        self.assertRaises(TypeError, BaseCalculator, 1)

if __name__ == '__main__':
    unittest.main()

