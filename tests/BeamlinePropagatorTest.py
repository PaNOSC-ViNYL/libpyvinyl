import unittest

from pyvinyl.BeamlinePropagator import BeamlinePropagator, BeamlinePropagatorParameters
from pyvinyl.BaseCalculator import BaseCalculator, BaseParameters


class BeamlinePropagatorParametersTest(unittest.TestCase):
    """
    Test class for the BeamlinePropagatorParametes class.
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

    def testDefaultConstruction(self):
        """ Testing the default construction of the class. """

        # Construct the object.
        parameters = BeamlinePropagatorParameters()

        # Test provenance.
        self.assertIsInstance(parameters, BeamlinePropagatorParameters)
        self.assertIsInstance(parameters, BaseParameters)

class BeamlinePropagatorTest(unittest.TestCase):
    """
    Test class for the BeamlinePropagator class.
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

    def testDefaultConstruction(self):
        """ Testing the default construction of the class. """

        # Construct the object.
        calculator = BeamlinePropagator()

        # Test provenance.
        self.assertIsInstance(calculator, BeamlinePropagator)
        self.assertIsInstance(calculator, BaseCalculator)

if __name__ == '__main__':
    unittest.main()

