"""
:module Instrument: Module hosting the Instrument class
"""

from libpyvinyl.Parameters.Collections import InstrumentParameters
from libpyvinyl import BaseCalculator
from libpyvinyl.BaseData import DataCollection

# typing
from libpyvinyl.Parameters.Collections import MasterParameters
from typing import Union, Any, Tuple, List, Dict, Optional


class Instrument:
    """Class collecting the parameters and calculators representing an entire instrument at a facility"""

    def __init__(
        self,
        name: str,
        calculators: Optional[Dict[str, BaseCalculator]] = None,
        instrument_base_dir: str = "./",
    ):
        """Instrument object initialization:

        :param name: The name of this instrument
        :param calculators: a collection of Calculator objects.
        """
        self.__name: str = ""
        self.__instrument_base_dir: str = ""
        self.__parameters = InstrumentParameters()

        self.name = name

        self.__calculators: Dict[str, BaseCalculator] = {}
        if calculators is not None:
            for calculator in calculators:
                self.add_calculator(calculator)

        self.set_instrument_base_dir(instrument_base_dir)

    def add_master_parameter(self, name: str, links: Dict[str, str], **kwargs) -> None:
        """
        Add a new parameter with the given name as master parameter.
        The goal is to link parameters in multiple calculators that represent the same quantity and that should be all changed at the same time when any of them is changed. This is obtained creating the link and by changing the value of the newly created master parameter.

        :param name: name of the master parameter
        :param links: dictionary with the names of the calculators and calculator parameters that represent the same quantity and hence can be changed all at once modifying the master parameter"
        """
        self.parameters.add_master_parameter(name, links, **kwargs)

    @property
    def name(self) -> str:
        """The name of this instrument."""
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if isinstance(value, str):
            self.__name = value
        else:
            raise TypeError(
                f"Instrument: name is expecting a str rather than {type(value)}"
            )

    @property
    def calculators(self) -> Dict[str, BaseCalculator]:
        """The list of calculators. It's modified either when constructing the class instance
        or using the :meth:`~libpyvinyl.Instrument.add_calculator` function.
        """
        return self.__calculators

    @property
    def parameters(self) -> InstrumentParameters:
        """
        The parameter collection of each calculator in the instrument.
        These parameters are links to the
        exact parameters of each calculator.
        """
        return self.__parameters

    @property
    def master(self) -> MasterParameters:
        """Return the master parameters"""
        return self.parameters.master

    @property
    def instrument_base_dir(self) -> str:
        return self.__instrument_base_dir

    @instrument_base_dir.setter
    def instrument_base_dir(self, value):
        self.set_instrument_base_dir(value)

    def set_instrument_base_dir(self, base: str) -> None:
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

    def __repr_calculators(self) -> str:
        """
        Return the list of all defined calculators for this instrument
        """
        string = f"- Instrument: {self.name} -\n"
        string += "Calculators:\n"
        for key in self.calculators:
            string += f"{key}\n"
        return string

    def list_calculators(self) -> None:
        """
        Print the list of all defined calculators for this instrument
        """
        string = self.__repr_calculators()
        print(string)

    def list_parameters(self) -> None:
        """
        Print the list of all calculator parameters
        """
        print(self.parameters)

    def add_calculator(self, calculator: BaseCalculator) -> None:
        """
        Append one calculator to the list of calculators.

        N.B. calculators are executed in the same order as they are provided

        :param calculator: calculator
        """
        self.__calculators[calculator.name] = calculator
        self.__parameters.add(calculator.name, calculator.parameters)

    def remove_calculator(self, calculator_name: str) -> None:
        """
        Remove the calculator with the given name from the list of calculators

        :param calculator_name: name of one calculator already added to the list
        """

        del self.__calculators[calculator_name]
        del self.__parameters[calculator_name]

    def run(self) -> None:
        """
        Run the entire simulation,
        i.e. all the calculators in the order they have been provided
        """
        for calculator in self.calculators.values():
            calculator.backengine()

    @property
    def output(self) -> DataCollection:
        """Return the output of the last calculator"""
        return list(self.__calculators.values())[-1].output

    def __str__(self) -> str:
        mystring = f"######## Instrument {self.name}\n"
        mystring += self.__repr_calculators()
        mystring += repr(self.parameters)
        mystring += f"############"
        return mystring
