import unittest
import numpy
import pytest
import os
import tempfile
from pint.quantity import Quantity
from pint.unit import Unit
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
        assert par.unit == str(Unit("cm"))
        self.assertEqual(par.comment, "comment string")

    def test_units_assignment(self):
        par = Parameter("test", unit="kg")
        assert par.unit == Unit("kg")
        par.unit = "cm"
        assert par.unit == Unit("cm")
        par.unit = "meter"
        assert par.unit == Unit("m")
        assert par.unit == str(Unit("m"))
        assert par.unit == "meter"
        par.unit = "nounit"
        assert par.unit == "nounit"

    def test_check_value_type(self):
        par = Parameter("test")
        v = 1
        par._Parameter__check_compatibility(v)
        par._Parameter__set_value_type(v)
        assert par._Parameter__value_type == int

        v = 1.0
        par._Parameter__check_compatibility(v)
        par._Parameter__set_value_type(v)
        assert par._Parameter__value_type == Quantity

        v = "string"
        with pytest.raises(TypeError):
            par._Parameter__check_compatibility(v)
        par._Parameter__set_value_type(v)
        assert par._Parameter__value_type == str

        v = True
        par = Parameter("test")
        par._Parameter__set_value_type("string")
        assert par._Parameter__value_type == str
        with pytest.raises(TypeError):
            par._Parameter__check_compatibility(v)

        par = Parameter("test")
        par._Parameter__set_value_type(True)
        assert par._Parameter__value_type == bool

        v = ["ciao", True]
        par = Parameter("test")
        with pytest.raises(TypeError):
            par._Parameter__check_compatibility(v)
        par._Parameter__set_value_type([False, True])

        v = {"ciao": True, "bye": "string"}
        par = Parameter("test")
        with pytest.raises(NotImplementedError):
            par._Parameter__check_compatibility(v)
        v = {"ciao": True, "bye": False}
        with pytest.raises(NotImplementedError):
            par._Parameter__check_compatibility(v)

        v = numpy.random.uniform(0, 1, 10)
        par = Parameter("test")
        par._Parameter__check_compatibility(v)
        par._Parameter__set_value_type(v)
        assert par._Parameter__value_type == Quantity

    # no conditions
    def test_parameter_no_legal_conditions(self):
        par = Parameter("test")
        self.assertTrue(par.is_legal(None))  # FIXME how is this supposed to work?
        self.assertTrue(par.is_legal(-999))
        self.assertTrue(par.is_legal(-1))
        self.assertTrue(par.is_legal(0))
        self.assertTrue(par.is_legal(1))
        self.assertTrue(par.is_legal("This is a string"))
        self.assertTrue(par.is_legal(True))
        self.assertTrue(par.is_legal(False))
        self.assertTrue(par.is_legal([0, "A", True]))

    # case 1: only legal interval
    def test_parameter_legal_interval(self):
        par = Parameter("test")
        par.add_interval(3, 4.5, True)

        self.assertTrue(par.is_legal(3.5))
        self.assertFalse(par.is_legal(1.0))

    # case 2: only illegal interval
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

    def test_values_different_types(self):
        par = Parameter("test")
        par.add_option(9.8, True)
        with pytest.raises(TypeError):
            par.add_option(True, True)

    def test_values_different_units(self):
        par = Parameter("energy", unit="meV", comment="Energy of emitted particles")
        import pint

        ureg = pint.UnitRegistry()
        with pytest.raises(pint.errors.DimensionalityError):
            thisunit = Unit("meter")
            par.value = 5 * thisunit

    # case 1: only legal option
    def test_parameter_legal_option_float(self):
        par = Parameter("test")
        par.add_option(9.8, True)

        self.assertFalse(par.is_legal(10))
        self.assertTrue(par.is_legal(9.8))
        self.assertFalse(par.is_legal(True))
        self.assertFalse(par.is_legal("A"))
        self.assertFalse(par.is_legal(38))

    # case 1: only legal option
    def test_parameter_legal_option_bool(self):
        par = Parameter("test")
        par.add_option(True, True)

        self.assertFalse(par.is_legal(10))
        self.assertFalse(par.is_legal(9.8))
        self.assertTrue(par.is_legal(True))
        self.assertFalse(par.is_legal("A"))
        self.assertFalse(par.is_legal(38))

    # case 1: only legal option
    def test_parameter_legal_option_float_and_int(self):
        par = Parameter("test")
        par.add_option(9.8, True)
        par.add_option(38, True)

        self.assertFalse(par.is_legal(10))
        self.assertTrue(par.is_legal(9.8))
        self.assertFalse(par.is_legal(True))
        self.assertFalse(par.is_legal("A"))
        self.assertTrue(par.is_legal(38))

    # case 1: only legal option
    def test_parameter_legal_option_int_and_float(self):
        par = Parameter("test")
        par.add_option(38, True)
        par.add_option(9.8, True)

        self.assertFalse(par.is_legal(10))
        self.assertTrue(par.is_legal(9.8))
        self.assertFalse(par.is_legal(True))
        self.assertFalse(par.is_legal("A"))
        self.assertTrue(par.is_legal(38))

    # case 1: only legal option
    def test_parameter_legal_option_fromlist(self):
        par = Parameter("test")
        par.add_option([9, 8, 38], True)

        self.assertFalse(par.is_legal(10))
        self.assertFalse(par.is_legal(9.8))
        self.assertFalse(par.is_legal(True))
        self.assertFalse(par.is_legal("A"))
        self.assertTrue(par.is_legal(38))
        self.assertTrue(par.is_legal(38.0))
        self.assertTrue(par.is_legal(8))

        # case 1: only legal option

    def test_parameter_legal_option_string(self):
        par = Parameter("test")
        par.add_option(["B", "A"], True)

        self.assertFalse(par.is_legal(10))
        self.assertFalse(par.is_legal(9.8))
        self.assertFalse(par.is_legal(True))
        self.assertTrue(par.is_legal("A"))
        self.assertTrue(par.is_legal("B"))
        self.assertFalse(par.is_legal("C"))
        self.assertFalse(par.is_legal(38))

    def test_parameter_multiple_options(self):
        par = Parameter("test")
        par.add_option(9.8, True)

        self.assertRaises(ValueError, par.add_option, 3, False)
        self.assertFalse(par.is_legal(-831.0))
        self.assertTrue(par.is_legal(9.8))
        self.assertFalse(par.is_legal(3))

    # case 1: legal interval + legal option
    def test_parameter_legal_interval_plus_legal_option(self):
        par = Parameter("test")
        par.add_interval(None, 8.5, True)  # minus infinite to 8.5
        par.add_option(5, True)  # this is stupid, already accounted in the interval
        par.add_option(11, True)

        self.assertTrue(par.is_legal(-831.0))
        self.assertTrue(par.is_legal(8.5))
        self.assertTrue(par.is_legal(5.0))
        self.assertFalse(par.is_legal(10.0))
        self.assertTrue(par.is_legal(11.0))

    # case 2: illegal interval + illegal option
    def test_parameter_illegal_interval_plus_illegal_option(self):
        par = Parameter("test")
        par.add_interval(None, 8.5, False)  # minus infinite to 8.5
        par.add_option(5, False)  # this is stupid, already accounted in the interval
        par.add_option(11, False)

        self.assertFalse(par.is_legal(-831.0))
        self.assertFalse(par.is_legal(8.5))  # illegal because closed interval
        self.assertFalse(par.is_legal(5.0))
        self.assertTrue(par.is_legal(10.0))
        self.assertFalse(par.is_legal(11.0))

    # case 3: legal interval + illegal option
    def test_parameter_legal_interval_plus_illegal_option(self):
        par = Parameter("test")
        par.add_interval(None, 8.5, True)  # minus infinite to 8.5
        par.add_option(5, False)

        self.assertTrue(par.is_legal(-831.0))
        self.assertTrue(par.is_legal(8.5))
        self.assertFalse(par.is_legal(5.0))
        self.assertFalse(par.is_legal(10.0))
        self.assertFalse(par.is_legal(11.0))

    # case 4: illegal interval + legal option
    def test_parameter_illegal_interval_plus_legal_option(self):
        par = Parameter("test")
        par.add_interval(None, 8.5, False)  # minus infinite to 8.5
        par.add_option(5, True)

        self.assertFalse(par.is_legal(-831.0))
        self.assertFalse(par.is_legal(8.5))
        self.assertTrue(par.is_legal(5.0))
        self.assertTrue(par.is_legal(10.0))
        self.assertTrue(par.is_legal(11.0))

    # case 2: illegal interval + illegal option
    def test_parameter_get_options(self):
        """
        Ensure get_options returns the options as required
        """
        par = Parameter("test")
        par.add_interval(None, 8.5, False)  # minus infinite to 8.5
        par.add_option(5, True)  # this is stupid, already accounted in the interval
        par.add_option(11, True)

        retrieved_options = par.get_options()

        self.assertEqual(len(retrieved_options), 2)
        self.assertEqual(retrieved_options[0], 5.0)
        self.assertEqual(retrieved_options[1], 11.0)
        self.assertTrue(par.get_options_are_legal())

    def test_parameter_value_type(self):
        par = Parameter("test")
        par.value = 4.0
        assert par._Parameter__value_type == Quantity

        par1 = Parameter("test")
        par1.value = 4
        assert par1._Parameter__value_type == int

        par2 = Parameter("test", unit="meV")
        par2.value = 4
        assert par2._Parameter__value_type == Quantity

        par3 = Parameter("test", unit="meV")
        par3.add_interval(0, 1e6, True)
        assert par3._Parameter__value_type == Quantity

    def test_parameter_set_value(self):
        par = Parameter("test")
        par.add_interval(3, 4.5, True)

        par.value = 4.0
        self.assertEqual(par.value, 4.0)

        with self.assertRaises(ValueError):
            par.value = 5.0  # Should throw an error and be ignored

        self.assertEqual(par.value, 4.0)

    def test_add_interval_after_value(self):
        par = Parameter("test")
        par.value = 4.0
        par.add_interval(3, 4.5, True)

        par.clear_intervals()
        par.value = 5.0
        with self.assertRaises(ValueError):
            par.add_interval(3, 4.5, True)

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
        par.print_parameter_constraints()

    def test_clear_intervals(self):  # FIXME
        par = Parameter("test")
        par.add_interval(3, 4.5, True)
        # self.assertEqual(par.__intervals, [[3, 4.5]]) #FIXME

        par.clear_intervals()
        par.add_option(9.7, True)
        #        self.assertEqual(par.__options, [9.7])
        par.clear_options()

    #        self.assertEqual(par.__options, [])

    def test_print_line(self):
        par = Parameter("test")
        par.add_interval(3, 4.5, True)
        par.add_option(9.8, True)
        par.print_line()

    def test_print(self):
        par = Parameter("test")
        par.add_interval(3, 4.5, True)
        par.add_option(9.8, True)
        print(par)

    def test_parameter_iterable(self):
        par = Parameter("test")
        par.add_interval(3, 4.5, True)
        par.add_option(7, True)
        self.assertFalse(par.is_legal([0.5, 3.2, 5.0]))
        self.assertTrue(par.is_legal([3.1, 4.2, 4.4]))
        self.assertTrue(par.is_legal([3.1, 4.2, 4.4, 7]))

    def test_get_intervals(self):
        par = Parameter("test")
        par.add_interval(3, 4.5, True)
        par.add_interval(8, 10, True)

        retrived_intervals = par.get_intervals()
        self.assertEqual(len(retrived_intervals), 2)
        self.assertEqual(retrived_intervals[0][0], 3)
        self.assertEqual(retrived_intervals[0][1], 4.5)
        self.assertEqual(retrived_intervals[1][0], 8)
        self.assertEqual(retrived_intervals[1][1], 10)

        self.assertTrue(par.get_intervals_are_legal())

    def test_parameters_with_quantity(self):
        """Test if we can construct and use a Parameter instance passing  pint.Quantity and pint.Unit objects to the constructor and interval setter."""

        # Define the base unit of my parameter object.
        meter = Unit("meter")
        self.assertIsInstance(meter, Unit)

        minimum_undulator_length = 10.0 * meter
        undulator_length = Parameter("undulator_length", meter)

        self.assertIsInstance(undulator_length, Parameter)
        self.assertEqual(undulator_length.unit, Unit("meter"))

        undulator_length.add_interval(
            min_value=minimum_undulator_length,
            max_value=numpy.inf * meter,
            intervals_are_legal=True,
        )

        self.assertTrue(undulator_length.is_legal(10.1 * meter))
        self.assertFalse(undulator_length.is_legal(9.0 * meter))
        self.assertTrue(undulator_length.is_legal(5.5e4 * Unit("centimeter")))

    def test_parameter_set_numpy_value(self):
        par = Parameter("test", unit="eV")
        par.value = 1e-4
        par.value = numpy.log(10)

    def test_parameters_with_quantity_powers(self):
        """Test if we can construct and use a Parameter instance passing  pint.Quantity and pint.Unit objects to the constructor and interval setter. Use different powers of 10 in parameter initialization and value assignment."""

        # Define the base unit of my parameter object.
        meter = Unit("meter")
        centimeter = Unit("centimeter")
        self.assertIsInstance(meter, Unit)

        minimum_undulator_length = 10.0 * meter
        undulator_length = Parameter("undulator_length", centimeter)

        self.assertIsInstance(undulator_length, Parameter)
        self.assertEqual(undulator_length.unit, Unit("centimeter"))

        undulator_length.add_interval(
            min_value=minimum_undulator_length,
            max_value=numpy.inf * meter,
            intervals_are_legal=True,
        )

        print(undulator_length)

        self.assertTrue(undulator_length.is_legal(10.1 * meter))
        self.assertFalse(undulator_length.is_legal(9.0 * centimeter))
        self.assertTrue(undulator_length.is_legal(5.5e4 * Unit("centimeter")))


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
        par1.value = 8.0
        par2 = Parameter("test2", unit="meV")
        par2.value = 10

        parameters = CalculatorParameters()
        parameters.add(par1)
        parameters.add(par2)

        with tempfile.TemporaryDirectory() as d:
            tmp_file = os.path.join(d, "test.json")
            parameters.to_json(tmp_file)
            params_json = CalculatorParameters.from_json(tmp_file)
            self.assertEqual(params_json["test2"].value, 10)
            assert params_json["test2"].value_no_conversion == Quantity(10, "meV")
            with pytest.raises(TypeError):
                params_json["test2"].value = "A"

    def test_json_with_objects(self):
        par1 = Parameter("test")
        par1.value = 8
        par2 = Parameter("test2", unit="meV")
        par2.value = 10
        par3 = Parameter("test3", unit="meV")
        par3.value = 3.14

        parameters = CalculatorParameters()
        parameters.add(par1)
        parameters.add(par2)
        parameters.add(par3)
        with tempfile.TemporaryDirectory() as d:
            tmp_file = os.path.join(d, "test.json")
            tmp_file = "/tmp/test.json"
            parameters.to_json(tmp_file)
            params_json = CalculatorParameters.from_json(tmp_file)
            self.assertEqual(params_json["test2"].value, 10)
            print(params_json["test3"])
            assert params_json["test3"].value == par3.value
            assert params_json["test3"].value == 3.14
            assert params_json["test3"].value_no_conversion == Quantity(3.14, "meV")

    def test_get_item(self):
        par1 = Parameter("test")
        par1.value = 8
        par2 = Parameter("test2", unit="meV")
        par2.value = 10

        parameters = CalculatorParameters()
        self.assertRaises(KeyError, parameters.__getitem__, "test3")


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
