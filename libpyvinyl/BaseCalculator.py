"""
:module BaseCalculator: Module hosting the BaseCalculator class.

"""

####################################################################################
#                                                                                  #
# This file is part of libpyvinyl - The APIs for Virtual Neutron and x-raY         #
# Laboratory.                                                                      #
#                                                                                  #
# Copyright (C) 2021  Carsten Fortmann-Grote, Juncheng E                           #
#                                                                                  #
# This program is free software: you can redistribute it and/or modify it under    #
# the terms of the GNU Lesser General Public License as published by the Free      #
# Software Foundation, either version 3 of the License, or (at your option) any    #
# later version.                                                                   #
#                                                                                  #
# This program is distributed in the hope that it will be useful, but WITHOUT ANY  #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A  #
# PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details. #
#                                                                                  #
# You should have received a copy of the GNU Lesser General Public License along   #
# with this program.  If not, see <https://www.gnu.org/licenses/                   #
#                                                                                  #
####################################################################################

from abc import abstractmethod
from typing import Union, Optional
from tempfile import mkstemp
import copy
import dill
from pathlib import Path
import logging
import os

from libpyvinyl.AbstractBaseClass import AbstractBaseClass
from libpyvinyl.BaseData import BaseData, DataCollection
from libpyvinyl.Parameters import CalculatorParameters

from typing import List

# if typing>= 3.11
# from typing import Self

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s", level=logging.WARNING
)


class BaseCalculator(AbstractBaseClass):
    """
    Base class of all calculators.

    This class provides the libpyvinyl API. It defines all methods
    through which a user interacts with the simulation backengines.

    This class is to be used as a base class for all calculators that implement
    a special simulation module, such as a photon diffraction calculator. Such a
    specialized Calculator has the same interface to the simulation
    backengine as all other ViNYL Calculators.

    A complete example including a instrument and calculators can be found in
    ``test/integration/plusminus``

    """

    def __init__(
        self,
        name: str,
        input: Union[DataCollection, List[BaseData], BaseData],
        output_keys: Union[list, str],
        output_data_types: Union[list, BaseData],
        output_filenames: Union[list, str, None] = None,
        instrument_base_dir: str = "./",
        calculator_base_dir: Optional[str] = None,
        parameters: CalculatorParameters = None,
    ):
        """
        Constructs this class.

        :param name: The name of this calculator.
        :param input: The input of this calculator. It can be a `DataCollection`,
                     a list of `BaseData`s or a single Data Object.

        :param output_keys: The key(s) of this calculator's output data.

        :param output_data_types: The data type(s), i.e., classes, of each output.
                                  It's a list of the data classes or a single data class.
                                  The available data classes are based on `BaseData`.
        :param output_filenames: The name(s) of the output file(s).
                                 It can be a str of a filename or a list of filenames.
                                 If the mapping is dict mapping, the name is `None`.
                                 Defaults to None.

        :param instrument_base_dir: The base directory for the instrument to which
                                    this calculator belongs.
                                    The final exact output file path depends on `instrument_base_dir` and `calculator_base_dir`: `instrument_base_dir`/`calculator_base_dir`/filename

        :param calculator_base_dir: The base directory for this calculator. The final
                                    exact output file path depends on `instrument_base_dir` and
                                    `calculator_base_dir`: `instrument_base_dir`/`calculator_base_dir`/filename

        :param parameters: The parameters for this calculator.

        """
        # Initialize the variables
        self.__name = None
        self.__instrument_base_dir = None
        self.__calculator_base_dir = None
        self.__input = None
        self.__output_keys = None
        self.__output_data_types = None
        self.__output_filenames = None
        self.__parameters = None
        self.__output: DataCollection = DataCollection()

        self.name = name
        self.input = input
        self.output_keys = output_keys
        self.output_data_types = output_data_types
        self.output_filenames = output_filenames
        self.instrument_base_dir = instrument_base_dir
        if calculator_base_dir is None:
            self.calculator_base_dir = name
        else:
            self.calculator_base_dir = calculator_base_dir
        self.parameters = parameters

        self.__check_consistency()
        # Create output data objects according to the output_data_classes
        self.__init_output()

    def __check_consistency(self):
        """Check the consistency of the input parameters"""
        if len(self.output_keys) != len(self.output_data_types):
            raise ValueError(
                f"len(output_keys) = {len(self.output_keys)} is not equal to len(output_data_types) = {len(self.output_data_types)}"
            )

    def __check_output_filenames(self):
        """Since output_filenames can be None for output in dict mapping, only check output_files when necessary"""
        if len(self.output_data_types) != len(self.output_filenames):
            raise ValueError(
                f"len(output_filenames) = {len(self.output_filenames)} is not equal to len(output_data_types) = {len(self.output_data_types)}"
            )

    @property
    def name(self) -> str:
        """The name of this calculator."""
        return self.__name

    @name.setter
    def name(self, value):
        if isinstance(value, str):
            self.__name = value
        else:
            raise TypeError(
                f"Calculator: `name` is expected to be a str, not {type(value)}"
            )

    @property
    def parameters(self) -> CalculatorParameters:
        """The parameters of this calculator."""
        return self.__parameters

    @parameters.setter
    def parameters(self, value: CalculatorParameters):
        self.reset_parameters(value)

    def reset_parameters(self, value: CalculatorParameters):
        """Resets the calculator parameters"""
        if isinstance(value, CalculatorParameters):
            self.__parameters = value
        elif value is None:
            self.init_parameters()
        else:
            raise TypeError(
                f"Calculator: `parameters` is expected to be CalculatorParameters, not {type(value)}"
            )

    def set_parameters(self, args_as_dict: bool = None, **kwargs):
        """
        Sets parameters contained in this calculator using dict or kwargs
        """
        if args_as_dict is not None:
            parameter_dict = args_as_dict
        else:
            parameter_dict = kwargs

        for key, parameter_value in parameter_dict.items():
            self.parameters[key].value = parameter_value

    @property
    def instrument_base_dir(self) -> str:
        """The base directory for the instrument to which this calculator belongs."""
        return self.__instrument_base_dir

    @instrument_base_dir.setter
    def instrument_base_dir(self, value):
        self.set_instrument_base_dir(value)

    def set_instrument_base_dir(self, value: str):
        """Set the instrument base directory"""
        if isinstance(value, str):
            self.__instrument_base_dir = value
        else:
            raise TypeError(
                f"Calculator: `instrument_base_dir` is expected to be a str, not {type(value)}"
            )

    @property
    def calculator_base_dir(self) -> str:
        """The base directory for this calculator. The final exact output file path depends on `instrument_base_dir` and
        `calculator_base_dir`: `instrument_base_dir`/`calculator_base_dir`/filename
        """
        return self.__calculator_base_dir

    @calculator_base_dir.setter
    def calculator_base_dir(self, value):
        self.set_calculator_base_dir(value)

    def set_calculator_base_dir(self, value: str):
        """Set the calculator base directory"""
        if isinstance(value, str):
            self.__calculator_base_dir = value
        else:
            raise TypeError(
                f"Calculator: `calculator_base_dir` is expected to be a str, not {type(value)}"
            )

    @property
    def input(self) -> DataCollection:
        """The input of this calculator. A collection or a single Data Object(s)."""
        return self.__input

    @input.setter
    def input(self, value):
        self.set_input(value)

    def set_input(self, value: Union[DataCollection, list, BaseData, None]):
        """Set the calculator input data. It can be a DataCollection, list or BaseData object."""
        if isinstance(value, (DataCollection, type(None))):
            self.__input = value
        elif isinstance(value, list):
            self.__input = DataCollection(*value)
        elif isinstance(value, BaseData):
            self.__input = DataCollection(value)
        else:
            raise TypeError(
                f"Calculator: `input` can be a DataCollection, list or BaseData object, and will be treated as a DataCollection. Your input type: {type(value)} is not accepted."
            )

    @property
    def output_keys(self) -> list:
        """The key(s) of this calculator's output data."""
        return self.__output_keys

    @output_keys.setter
    def output_keys(self, value):
        self.set_output_keys(value)

    @property
    def base_dir(self):
        """The base path for the output files of this calculator in consideration of instrument_base_dir and calculator_base_dir"""
        base_dir = Path(self.instrument_base_dir) / self.calculator_base_dir
        return str(base_dir)

    @property
    def output_file_paths(self):
        """The final output file paths considering base_dir"""
        self.__check_output_filenames()
        paths = []

        for filename in self.output_filenames:
            path = Path(self.base_dir) / filename
            # Make sure the file directory exists
            path.parent.mkdir(parents=True, exist_ok=True)
            paths.append(str(path))
        return paths

    def set_output_keys(self, value: Union[list, str]):
        """Set the calculator output keys. It can be a list of str or a single str."""
        if isinstance(value, list):
            for item in value:
                assert type(item) is str
            self.__output_keys = value
        elif isinstance(value, str):
            self.__output_keys = [value]
        else:
            raise TypeError(
                f"Calculator: `output_keys` can be a list or str, and will be treated as a list. Your input type: {type(value)} is not accepted."
            )

    @property
    def output_data_types(self) -> list:
        """The data type(s), i.e., classes, of each output."""
        return self.__output_data_types

    @output_data_types.setter
    def output_data_types(self, value):
        self.set_output_data_types(value)

    def set_output_data_types(self, value: Union[list, BaseData]):
        """Set the calculator output data type. It can be a list of DataClass or a single DataClass."""
        if isinstance(value, list):
            for item in value:
                assert issubclass(item, BaseData)
            self.__output_data_types = value
        elif issubclass(value, BaseData):
            self.__output_data_types = [value]
        else:
            raise TypeError(
                f"Calculator: `output_data_types` can be a list or a subclass of BaseData, and will be treated as a list. Your input type: {type(value)} is not accepted."
            )

    @property
    def output_filenames(self) -> list:
        """The name(s) of the output file(s). It can be a str of a filename or a list of filenames. If the mapping is dict mapping, the name is `None`."""
        return self.__output_filenames

    @output_filenames.setter
    def output_filenames(self, value):
        self.set_output_filenames(value)

    def set_output_filenames(self, value: Union[list, str, None]):
        """Set the calculator output filenames. It can be a list of filenames or just a single str."""
        if isinstance(value, list):
            for item in value:
                assert type(item) is str or type(None)
            self.__output_filenames = value
        elif isinstance(value, (str, type(None))):
            self.__output_filenames = [value]
        else:
            raise TypeError(
                f"Calculator: `output_filenames` can be a list or just a str or None, and will be treated as a list. Your input type: {type(value)} is not accepted."
            )

    @property
    def output(self):
        """The output of this calculator"""
        return self.__output

    @property
    def data(self):
        """The alias of output. It's not recommended to use this variable name due to it's ambiguity."""
        return self.__output

    @abstractmethod
    def init_parameters(self):
        """Virtual method to initialize all parameters. Must be implemented on the
        specialized class."""

        raise NotImplementedError

    def __init_output(self):
        """Create output data objects according to the output_data_types"""
        output = DataCollection()
        for i, key in enumerate(self.output_keys):
            output_data = self.output_data_types[i](key)
            output.add_data(output_data)
        self.__output = output

    def __call__(self, parameters=None, **kwargs):
        """The copy constructor

        :param parameters: The parameters for the new calculator.
        :type  parameters: CalculatorParameters

        :param kwargs: key-value pairs of parameters to change in the new instance.

        :return: A new parameters instance with optionally changed parameters.

        """

        new = copy.deepcopy(self)

        new.__dict__.update(kwargs)

        if parameters is None:
            new.parameters = copy.deepcopy(new.parameters)
        else:
            new.parameters = parameters
        return new

    @classmethod
    def from_dump(cls, dumpfile: str):
        """Load a dill dump from a dumpfile.

        :param dumpfile: The file name of the dumpfile.
        :return: The calculator object restored from the dumpfile.

        """

        with open(dumpfile, "rb") as fhandle:
            try:
                tmp = dill.load(fhandle)
            except:
                raise IOError("Cannot load calculator from {}.".format(dumpfile))

            if not isinstance(tmp, cls):
                raise TypeError(f"The object in the file {dumpfile} is not a {cls}")

        return tmp

    def dump(self, fname: Optional[str] = None) -> str:
        """
        Dump class instance to file.

        :param fname: Filename (path) of the file to write.
        :return: The filename of the dumpfile
        """

        if fname is None:
            _, fname = mkstemp(
                suffix="_dump.dill",
                prefix=self.__class__.__name__[-1],
                dir=os.getcwd(),
            )
        with open(fname, "wb") as file_handle:
            dill.dump(self, file_handle)

        return fname

    @abstractmethod
    def backengine(self):
        """Execute the intended operation of this class."""
        raise NotImplementedError


# This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 823852.
