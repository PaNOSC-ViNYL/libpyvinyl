"""
:module Instrument: Module hosting the Instrument class
"""

from libpyvinyl.Parameters.Collections import InstrumentParameters
from pathlib import Path


class Instrument:
    """An Instrument class"""

    def __init__(self, name, calculators=None):
        """An Instrument class

        :param name: The name of this instrument
        :type name: str
        :param calculators: A collection of Calculator objects.
        :type calculators: dict
        """
        self.__name = name
        self.__calculators = {}
        self.__parameters = InstrumentParameters()
        if calculators is not None:
            for calculator in calculators:
                self.add_calculator(calculator)

    def add_master_parameter(self, name, links, **kwargs):
        self.parameters.add_master_parameter(name, links, **kwargs)

    @property
    def name(self):
        """The name of this instrument."""
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

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

    def set_base_path(self, base: str):
        """Set each calculator's output_path as 'base_path/calculator.name'.

        :param base: The base path to be set.
        :type base: str
        """
        self.base_path = base
        basePath = Path(base)
        for key in self.calculators:
            outputPath = basePath / self.calculators[key].name
            calculator = self.calculators[key]
            calculator.output_path = str(outputPath)

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
