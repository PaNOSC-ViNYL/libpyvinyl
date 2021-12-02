import unittest
import os
import tempfile

from libpyvinyl.Parameters import Parameter
from libpyvinyl.Parameters import CalculatorParameters
from libpyvinyl.Parameters import InstrumentParameters


class Test_Parameter(unittest.TestCase):
    def test_initialize_parameter_simple(self):
        par = Parameter("test")
        self.assertEqual(par.name, "test")

    def test_initialize_parameter_complex(self):
        par = Parameter("test", unit="cm", comment="comment string")
        self.assertEqual(par.name, "test")
        self.assertEqual(par.unit, "cm")
        self.assertEqual(par.comment, "comment string")

    def test_parameter_legal_interval(self):
        par = Parameter("test")
        par.add_interval(3, 4.5, True)

        self.assertTrue(par.is_legal(3.5))
        self.assertFalse(par.is_legal(1.0))

    def test_parameter_illegal_interval(self):
        par = Parameter("test")
        par.add_interval(3, 4.5, False)

        self.assertFalse(par.is_legal(3.5))
        self.assertTrue(par.is_legal(1.0))

    def test_parameter_multiple_intervals(self):
        par = Parameter("test")
        par.add_interval(None, 8.5, True)  # minus infinite to 8.5

        self.assertRaises(ValueError, par.add_interval, 3, 4.5, False)
        self.assertTrue(par.is_legal(-831.0))
        self.assertTrue(par.is_legal(3.5))
        self.assertTrue(par.is_legal(5.0))
        self.assertFalse(par.is_legal(10.0))

    def test_parameter_option(self):
        par = Parameter("test")
        par.add_option(9.8, True)
        par.add_option(True, True)
        par.add_option(["A", 38], True)

        self.assertFalse(par.is_legal(10))
        self.assertTrue(par.is_legal(9.8))
        self.assertTrue(par.is_legal(True))
        self.assertTrue(par.is_legal("A"))
        self.assertTrue(par.is_legal(38))

    def test_parameter_multiple_options(self):
        par = Parameter("test")
        par.add_option(9.8, True)

        self.assertRaises(ValueError, par.add_option, 3, False)
        self.assertFalse(par.is_legal(-831.0))
        self.assertTrue(par.is_legal(9.8))
        self.assertFalse(par.is_legal(3))

    def test_parameter_legal_interval_plus_option(self):
        par = Parameter("test")
        par.add_interval(None, 8.5, True)  # minus infinite to 8.5
        # par.add_illegal_interval(3, 4.5)
        par.add_option(11, True)

        self.assertTrue(par.is_legal(-831.0))
        self.assertFalse(par.is_legal(8.5))
        self.assertTrue(par.is_legal(5.0))
        self.assertFalse(par.is_legal(10.0))
        self.assertTrue(par.is_legal(11.0))

    def test_parameter_illegal_interval_plus_option(self):
        par = Parameter("test")
        par.add_interval(None, 8.5, False)  # minus infinite to 8.5
        # par.add_illegal_interval(3, 4.5)
        par.add_option(11, True)

        self.assertFalse(par.is_legal(-831.0))
        self.assertTrue(par.is_legal(8.5))
        self.assertFalse(par.is_legal(5.0))
        self.assertTrue(par.is_legal(10.0))
        self.assertTrue(par.is_legal(11.0))

    def test_parameter_legal_interval_plus_illegal_option(self):
        par = Parameter("test")
        par.add_interval(None, 8.5, True)  # minus infinite to 8.5

        # par.add_illegal_interval(3, 4.5)
        par.add_option(5, False)

        self.assertTrue(par.is_legal(-831.0))
        self.assertFalse(par.is_legal(8.5))
        self.assertFalse(par.is_legal(5.0))
        self.assertFalse(par.is_legal(10.0))
        self.assertFalse(par.is_legal(11.0))

    def test_parameter_set_value(self):
        par = Parameter("test")
        par.add_interval(3, 4.5, True)

        par.value = 4.0
        self.assertEqual(par.value, 4.0)

        with self.assertRaises(ValueError):
            par.value = 5.0  # Should throw an error and be ignored

        self.assertEqual(par.value, 4.0)

    def test_parameter_from_dict(self):
        par = Parameter("test")

        par.add_interval(3, 4.5, True)
        par.value = 4.0
        par_from_dict = Parameter.from_dict(par.__dict__)
        self.assertEqual(par_from_dict.value, 4.0)

    def test_print_legal_interval(self):
        par = Parameter("test")
        par.add_interval(3, 4.5, True)
        par.add_option(9.8, True)
        par.print_paramter_constraints()

    def test_clear_intervals(self):  # FIXME
        par = Parameter("test")
        par.add_interval(3, 4.5, True)
        self.assertEqual(par.intervals, [[3, 4.5]])
        # par.add_illegal_interval(5, 10)
        # self.assertEqual(par.illegal_intervals, [[5, 10]])
        par.clear_intervals()
        # self.assertEqual(par.legal_intervals, [])
        # par.clear_illegal_intervals()
        # self.assertEqual(par.illegal_intervals, [])
        par.add_option(9.7, True)
        self.assertEqual(par.options, [9.7])
        par.clear_options()
        self.assertEqual(par.options, [])

    def test_print_line(self):
        par = Parameter("test")
        par.add_legal_interval(3, 4.5)
        par.add_option(9.8)
        par.print_line()

    def test_print(self):
        par = Parameter("test")
        par.add_legal_interval(3, 4.5)
        par.add_option(9.8)
        print(par)

    def test_parameter_iterable(self):
        par = Parameter("test")
        par.add_interval(3, 4.5, True)
        par.add_option(7, True)
        self.assertFalse(par.is_legal([0.5, 3.2, 5.0]))
        self.assertTrue(par.is_legal([3.1, 4.2, 4.4]))
        self.assertTrue(par.is_legal([3.1, 4.2, 4.4, 7]))


class Test_Parameters(unittest.TestCase):
    def test_initialize_parameters_from_list(self):
        par1 = Parameter("test")
        par1.value = 8
        par2 = Parameter("test2", unit="meV")

        parameters = CalculatorParameters([par1, par2])

        self.assertEqual(parameters["test"].value, 8)

    def test_initialize_parameters_from_add(self):
        par1 = Parameter("test")
        par1.value = 8
        par2 = Parameter("test2", unit="meV")
        par2.value = 10

        parameters = CalculatorParameters()
        parameters.add(par1)
        parameters.add(par2)

        self.assertEqual(parameters["test"].value, 8)
        self.assertEqual(parameters["test2"].value, 10)

    def test_print_parameters(self):
        par1 = Parameter("test")
        par1.value = 8
        par2 = Parameter("test2", unit="meV")
        par2.value = 10
        parameters = CalculatorParameters()
        parameters.add(par1)
        parameters.add(par2)
        print(parameters)

    def test_json(self):
        par1 = Parameter("test")
        par1.value = 8
        par2 = Parameter("test2", unit="meV")
        par2.value = 10

        parameters = CalculatorParameters()
        parameters.add(par1)
        parameters.add(par2)
        with tempfile.TemporaryDirectory() as d:
            tmp_file = os.path.join(d, "test.json")
            # tmp_file = 'test.json'
            parameters.to_json(tmp_file)
            params_json = CalculatorParameters.from_json(tmp_file)
            self.assertEqual(params_json["test2"].value, 10)


def source_calculator():
    """
    Little dummy calculator that sets up a parameters object for a source
    """
    parameters = CalculatorParameters()
    parameters.new_parameter("energy", unit="eV", comment="Source energy setting")
    parameters["energy"].add_interval(0, 1e6, True)
    parameters["energy"].value = 4000

    parameters.new_parameter("delta_energy", unit="eV", comment="Energy spread fwhm")
    parameters["delta_energy"].add_interval(0, 400, True)

    parameters.new_parameter("position", unit="cm", comment="Source center")
    parameters["position"].add_interval(-1.5, 1.5, True)

    parameters.new_parameter("gaussian", comment="False for flat, True for gaussian")
    parameters["gaussian"].add_option([False, True], True)

    return parameters


def sample_calculator():
    """
    Little dummy calculator that sets up a parameters object for a sample
    """
    parameters = CalculatorParameters()
    parameters.new_parameter("radius", unit="cm", comment="Sample radius")
    parameters["radius"].add_interval(0, None, True)  # To infinite

    parameters.new_parameter("height", unit="cm", comment="Sample height")
    parameters["height"].add_interval(0, None, True)

    absporption = parameters.new_parameter(
        "absorption", unit="barns", comment="absorption cross section"
    )
    absporption.add_interval(0, None, True)

    return parameters


class Test_Instruments(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setting up the test class."""
        cls.d = tempfile.TemporaryDirectory()

    def setUp(self):
        # We start creating our instrument with a InstrumentParameters
        self.instr_parameters = InstrumentParameters()

        # We insert a source and get some parameters out
        source_pars = source_calculator()
        # These are added to the instr_parameters so they can be controlled
        self.instr_parameters.add("Source", source_pars)

        # We also add a few sample objects with their parameter objects
        top_sample_pars = sample_calculator()
        self.instr_parameters.add("Sample top", top_sample_pars)

        bottom_sample_pars = sample_calculator()
        self.instr_parameters.add("Sample bottom", bottom_sample_pars)

    @classmethod
    def tearDownClass(cls):
        """Tearing down the test class."""
        cls.d.cleanup()

    def test_link(self):
        description = "Absorption cross section for both samples"
        links = {"Sample top": "absorption", "Sample bottom": "absorption"}
        master_value = 3.4
        self.instr_parameters.add_master_parameter(
            "absorption", links, unit="barns", comment=description
        )
        self.instr_parameters.master["absorption"] = master_value
        top_value = self.instr_parameters["Sample top"]["absorption"].value
        bottom_value = self.instr_parameters["Sample bottom"]["absorption"].value
        self.assertEqual(top_value, master_value)
        self.assertEqual(bottom_value, master_value)
        master_params = self.instr_parameters.master.parameters
        self.assertIn("absorption", master_params.keys())
        self.assertEqual(master_value, master_params["absorption"].value)
        self.assertEqual(self.instr_parameters.master["absorption"].links, links)

    def test_print(self):
        print(self.instr_parameters)

    def test_json(self):
        description = "Absorption cross section for both samples"
        links = {"Sample top": "absorption", "Sample bottom": "absorption"}
        master_value = 3.4
        self.instr_parameters.add_master_parameter(
            "absorption", links, unit="barns", comment=description
        )
        self.instr_parameters.master["absorption"] = master_value
        temp_file = os.path.join(self.d.name, "test.json")
        # temp_file = 'instrument.json'
        self.instr_parameters.to_json(temp_file)
        print(self.instr_parameters)

        # From json
        instr_json = InstrumentParameters.from_json(temp_file)
        self.assertEqual(instr_json["Source"]["energy"].value, 4000)
        master_params = instr_json.master.parameters
        self.assertIn("absorption", master_params.keys())
        self.assertEqual(master_value, master_params["absorption"].value)
        self.assertEqual(self.instr_parameters.master["absorption"].links, links)


if __name__ == "__main__":
    unittest.main()
