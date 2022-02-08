"""
:module Instrument: Module hosting the Instrument class
"""

from libpyvinyl.Parameters.Collections import InstrumentParameters


class Instrument:
    """An Instrument class"""

    def __init__(self, name, calculators=None, instrument_base_dir="./"):
        """An Instrument class

        :param name: The name of this instrument
        :type name: str
        :param calculators: A collection of Calculator objects.
        :type calculators: dict
        """
        self.__name = None
        self.__instrument_base_dir = None
        self.__parameters = InstrumentParameters()

        self.name = name

        self.__calculators = {}
        if calculators is not None:
            for calculator in calculators:
                self.add_calculator(calculator)

        self.set_instrument_base_dir(instrument_base_dir)

    def add_master_parameter(self, name, links, **kwargs):
        self.parameters.add_master_parameter(name, links, **kwargs)

    @property
    def name(self):
        """The name of this instrument."""
        return self.__name

    @name.setter
    def name(self, value: str):
        if isinstance(value, str):
            self.__name = value
        else:
            raise TypeError(
                f"Instrument: name is expecting a str rather than {type(value)}"
            )

    @property
    def calculators(self):
        """The list of calculators. It's modified either when constructing the class instance
        or using the `add_calculator` function.
        """
        return self.__calculators

    @property
    def parameters(self):
        """The parameter collection of each calculator in the instrument. These parameters are links to the
        exact parameters of each calculator."""
        return self.__parameters

    @property
    def master(self):
        return self.parameters.master

    def set_instrument_base_dir(self, base: str):
        """Set each calculator's `instrument_base_dir` to '`base`. Each calculator's data file ouput directory
        will be "`instrument_base_dir`/`calculator_base_dir`".

        :param base: The base directory to be set.
        :type base: str
        """
        if isinstance(base, str):
            self.__instrument_base_dir = base
            for calculator in self.calculators.values():
                calculator.instrument_base_dir = self.__instrument_base_dir
        else:
            raise TypeError(
                f"Instrument: instrument_base_dir is expecting a str rather than {type(base)}"
            )

    def list_calculators(self):
        string = f"- Instrument: {self.name} -\n"
        string += "Calculators:\n"
        for key in self.calculators:
            string += f"{key}\n"
        print(string)

    def list_parameters(self):
        print(self.parameters)

    def add_calculator(self, calculator):
        self.__calculators[calculator.name] = calculator
        self.__parameters.add(calculator.name, calculator.parameters)

    def remove_calculator(self, calculator_name):
        del self.__calculators[calculator_name]
        del self.__parameters[calculator_name]

    def run(self):
        for calculator in self.calculators.values():
            calculator.backengine()
