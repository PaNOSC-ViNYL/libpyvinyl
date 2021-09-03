"""
:module Instrument: Module hosting the Instrument class
"""

from libpyvinyl.Parameters.Collections import InstrumentParameters
from pathlib import Path


class Instrument():
    """An Instrument class"""
    def __init__(self, name, calculators=None):
        """An Instrument class

        :param name: The name of this instrument
        :type name: str
        :param calculators: A collection of Calculator objects.
        :type calculators: list
        """
        self.name = name
        self.calculators = {}
        self.parameters = InstrumentParameters()
        if calculators is not None:
            for calculator in calculators:
                self.add_calculator(calculator)

    def add_master_parameter(self, name, links, **kwargs):
        self.parameters.add_master_parameter(name, links, **kwargs)

    @property
    def master(self):
        return self.parameters.master

    def set_base_path(self, base: str):
        """Set each calculator's output_path as 'base_path/calculator.name'.

        Args:
            base (str): The base path to be set.
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
        self.calculators[calculator.name] = calculator
        self.parameters.add(calculator.name, calculator.parameters)

    def remove_calculator(self, calculator_name):
        del self.calculators[calculator_name]
        del self.parameters[calculator_name]
