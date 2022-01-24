import unittest
import os
import shutil

from libpyvinyl.BaseCalculator import SpecializedCalculator
from libpyvinyl.Instrument import Instrument


class InstrumentTest(unittest.TestCase):
    """
    Test class for the Detector class.
    """
    @classmethod
    def setUpClass(cls):
        """ Setting up the test class. """
        calculator1 = SpecializedCalculator('test1')
        calculator1.setParams()
        cls.calculator1 = calculator1
        calculator2 = SpecializedCalculator('test2')
        calculator2.setParams(12, 0.002)
        cls.calculator2 = calculator2

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

    def testInstrumentConstruction(self):
        """ Testing the default construction of the class. """

        # Construct the object.
        my_instrument = Instrument('myInstrument')
        my_instrument.add_calculator(self.calculator1)
        my_instrument.add_calculator(self.calculator2)

    def testListCalculator(self):
        """ Testing list calculators """

        # Construct the object.
        my_instrument = Instrument('myInstrument')
        my_instrument.add_calculator(self.calculator1)
        my_instrument.add_calculator(self.calculator2)
        my_instrument.list_calculators()

    def testListParams(self):
        """ Testing listing parameters """

        my_instrument = Instrument('myInstrument')
        calculator1 = SpecializedCalculator('test1')
        calculator1.setParams()
        calculator2 = SpecializedCalculator('test2')
        calculator2.setParams(12, 0.002)
        my_instrument.add_calculator(calculator1)
        my_instrument.add_calculator(calculator2)
        my_instrument.list_parameters()

    def testRemoveCalculator(self):
        """ Testing remove calculator """

        my_instrument = Instrument('myInstrument')
        my_instrument.add_calculator(self.calculator1)
        my_instrument.add_calculator(self.calculator2)
        self.assertEqual(len(my_instrument.calculators), 2)
        my_instrument.remove_calculator(self.calculator1.name)
        self.assertEqual(len(my_instrument.calculators), 1)

    def testEditCalculator(self):
        """ Testing edit calculator """
        my_instrument = Instrument('myInstrument')
        my_instrument.add_calculator(self.calculator1)
        my_instrument.parameters['test1']['photon_energy'] = 15
        energy1 = my_instrument.calculators['test1'].parameters[
            'photon_energy'].value
        self.assertEqual(energy1, 15)

    def testAddMaster(self):
        """ Testing remove calculator """

        my_instrument = Instrument('myInstrument')
        my_instrument.add_calculator(self.calculator1)
        my_instrument.add_calculator(self.calculator2)
        links = {'test1': 'photon_energy', 'test2': 'photon_energy'}
        my_instrument.add_master_parameter('photon_energy', links)
        my_instrument.master['photon_energy'] = 10
        energy1 = my_instrument.calculators['test1'].parameters[
            'photon_energy'].value
        energy2 = my_instrument.calculators['test2'].parameters[
            'photon_energy'].value
        self.assertEqual(energy1, 10)
        self.assertEqual(energy2, 10)

    # def testSetBasePath(self):
        # """ Testing setup base path for calculators """

        # my_instrument = Instrument('myInstrument')
        # my_instrument.add_calculator(self.calculator1)
        # my_instrument.add_calculator(self.calculator2)
        # my_instrument.set_instrument_base_dir('test')
        # self.assertEqual(my_instrument.calculators["test1"].output_path,
                         # 'test/test1')
        # self.assertEqual(my_instrument.calculators["test2"].output_path,
                         # 'test/test2')


if __name__ == '__main__':
    unittest.main()
