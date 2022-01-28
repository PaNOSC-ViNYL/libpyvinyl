"""
:module BaseCalculator: Module hosting the BaseCalculator and Parameters classes.

"""

####################################################################################
#                                                                                  #
# This file is part of libpyvinyl - The APIs for Virtual Neutron and x-raY            #
# Laboratory.                                                                      #
#                                                                                  #
# Copyright (C) 2020  Carsten Fortmann-Grote                                       #
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
from typing import Union
from libpyvinyl.AbstractBaseClass import AbstractBaseClass
from libpyvinyl.BaseData import BaseData, DataCollection

from libpyvinyl.Parameters import CalculatorParameters

from tempfile import mkstemp
import copy
import dill
import h5py
import sys
import logging
import os

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(message)s", level=logging.WARNING
)


class BaseCalculator(AbstractBaseClass):
    """

    :class BaseCalculator: Base class of all calculators.

    This class is provides the libpyvinyl API. It defines all methods
    through which a user interacts with the simulation backengines.

    This class is to be used as a base class for all calculators that implement
    a special simulation module, such as a photon diffraction calculator. Such a
    specialized Calculator has the same interface to the simulation
    backengine as all other ViNYL Calculators.

    A Complete example including a instrument and calculators can be found in
    `test/integration/plusminus`

    """
    def __init__(self, name: str, input: Union[DataCollection, list, BaseData],
        output_keys: Union[list, str],
        output_data_classes: list,
        output_filenames: Union[list, str] = None,
        instrument_base_dir="./",
        calculator_base_dir="BaseCalculator",
        parameters=None, dumpfile:str=None):
        """

        :param name: The name of this calculator.
        :type name: str

        :param name: The input of this caluclator. It can be a `DataCollection`,
        a list of `DataCollection`s or a single Data Object.
        :type name: DataCollection, list or BaseData

        :param output_keys: The key(s) of this caluclator's output data. It's a list of `str`s or
        a single str.
        :type output_keys: list or str

        :param output_data_classes: The data class(es) of each output. It's a list of the
        data classes or a single data class. The available data classes are based on `BaseData`.
        :type output_data_classes: list or DataClass

        :param output_filenames: The name(s) of the output file(s). It can be a str of a filename or
        a list of filenames. If the mapping is dict mapping, the name is `None`. Defaults to None.
        :type output_filenames: list or str

        :param instrument_base_dir: The base directory for the instrument to which this calculator
        belongs. Defaults to "./". The final exact output file path depends on `instrument_base_dir`
        and `calculator_base_dir`: `instrument_base_dir`/`calculator_base_dir`/filename
        :type instrument_base_dir: str

        :param calculator_base_dir: The base directory for this calculator. Defaults to "./". The final
        exact output file path depends on `instrument_base_dir` and
        `calculator_base_dir`: `instrument_base_dir`/`calculator_base_dir`/filename
        :type instrument_base_dir: str

        :param parameters: The parameters for this calculator.
        :type  parameters: Parameters

        :param dumpfile: If given, load a previously dumped (aka pickled) calculator.
        :type dumpfile: str

        :param kwargs: (key, value) pairs of further arguments to the calculator, e.g input_path, output_path.

        If both 'parameters' and 'dumpfile' are given, the dumpfile is loaded
        first. Passing a parameters object may be used to update some
        parameters.

        TODO:
        Example:
        ```
        # Define a specialized calculator.
        class MyCalculator(BaseCalculator):

            def __init__(self, parameters=None, dumpfile=None, **kwargs):
                super()__init__(parameters, dumpfile, **kwargs)

            def backengine(self):
                os.system("my_simulation_backengine_call")

            def saveH5(self):
                # Format output into openpmd hdf5 format.

        class MyParameters(Parameters):
            pass

        my_calculator = MyCalculator(my_parameters)

        my_calculator.backengine()

        my_calculator.saveH5("my_sim_output.h5")
        my_calculater.dump("my_calculator.dill")
        ```

        """
        self.__name = None
        self.__instrument_base_dir = None
        self.__calculator_base_dir = None
        self.__input = None
        self.__input_keys = None
        self.__output_keys = None
        self.__output_data_classes = None
        self.__output_filenames = None
        self.__parameters = None

        self.name = name
        self.input = input
        self.output_keys = output_keys
        self.output_data_types = output_data_classes
        self.output_filenames = output_filenames
        self.instrument_base_dir = instrument_base_dir
        self.calculator_base_dir = calculator_base_dir
        self.parameters = parameters
    
        # Create output data objects according to the output_data_classes
        self.__init_output()

    @property
    def name(self):
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
    def parameters(self):
        return self.__parameters

    @parameters.setter
    def parameters(self, value):
        if isinstance(value, CalculatorParameters):
            self.__parameters = value
        elif value is None:
            self.init_parameters()
        else:
            raise TypeError(
                f"Calculator: `parameters` is expected to be CalculatorParameters, not {type(value)}"
            )

    @property
    def input(self):
        return self.__input

    @input.setter
    def input(self, value):
        self.set_input(value)

    def set_input(self, value: Union[DataCollection, list, BaseData]):
        if isinstance(value, DataCollection):
            self.__input = value
        elif isinstance(value, list):
            self.__input = DataCollection(*value)
        elif isinstance(value, BaseData):
            self.__input = DataCollection(value)
        else:
            raise TypeError(
                f"Calculator: `input` can be a  DataCollection, list or BaseData object, and will be treated as a DataCollection, but not {type(value)}"
            )

    @property
    def input_keys(self):
        return self.__input_keys

    @input_keys.setter
    def input_keys(self, value):
        self.set_input_keys(value)

    def set_input_keys(self, value: Union[list, str]):
        if isinstance(value, list):
            for item in value:
                assert type(item) is str
            self.__input_keys = value
        elif isinstance(value, str):
            self.__input_keys = [value]
        else:
            raise TypeError(
                f"Calculator: `input_keys` can be a list or a string, and will be treated as a list, but not {type(value)}"
            )

    @property
    def output_keys(self):
        return self.__output_keys

    @output_keys.setter
    def output_keys(self, value):
        self.set_output_keys(value)

    def set_output_keys(self, value: Union[list, str]):
        if isinstance(value, list):
            for item in value:
                assert type(item) is str
            self.__output_keys = value
        elif isinstance(value, str):
            self.__output_keys = [value]
        else:
            raise TypeError(
                f"Calculator: `output_keys` can be a list or a string, and will be treated as a list, but not {type(value)}"
            )


    #TODO: Add example codes
    @abstractmethod
    def init_parameters(self):
        raise NotImplementedError

    def __init_output(self):
        """Create output data objects according to the output_data_classes"""
        output = DataCollection()
        for i, key in enumerate(self.output_keys):
            output_data = self.output_data_types[i](key)
            output.add_data(output_data)
        self.output = output

    def __call__(self, parameters=None, **kwargs):
        """The copy constructor

        :param parameters: The parameters for the new calculator.
        :type  parameters: CalculatorParameters

        :param kwargs: key-value pairs of parameters to change in the new instance.

        :return: A new parameters instance with optionally changed parameters.

        """

        new = copy.deepcopy(self)

        new.__dict__.update(kwargs)

        if parameters is not None:
            new.parameters = parameters

        return new

    # TODO: modify to from dump
    @classmethod
    def __load_from_dump(self, dumpfile):
        """ """
        """
        Load a dill dump and initialize self's internals.

        """

        with open(dumpfile, "rb") as fhandle:
            try:
                tmp = dill.load(fhandle)
            except:
                raise IOError("Cannot load calculator from {}.".format(dumpfile))

        self.__dict__ = copy.deepcopy(tmp.__dict__)

        del tmp

    @property
    def parameters(self):
        """The parameters of this calculator."""

        return self.__parameters

    @parameters.setter
    def parameters(self, val):

        if not isinstance(val, (type(None), CalculatorParameters)):
            raise TypeError(
                """Passed argument 'parameters' has wrong type. Expected CalculatorParameters, found {}.""".format(
                    type(val)
                )
            )

        self.__parameters = val

    def set_parameters(self, args_as_dict=None, **kwargs):
        """
        Sets parameters contained in this calculator using dict or kwargs
        """
        if args_as_dict is not None:
            parameter_dict = args_as_dict
        else:
            parameter_dict = kwargs

        for key, parameter_value in parameter_dict.items():
            self.parameters[key].value = parameter_value

    def dump(self, fname=None):
        """
        Dump class instance to file.

        :param fname: Filename (path) of the file to write.

        """

        if fname is None:
            _, fname = mkstemp(
                suffix="_dump.dill",
                prefix=self.__class__.__name__[-1],
                dir=os.getcwd(),
            )
        try:
            with open(fname, "wb") as file_handle:
                dill.dump(self, file_handle)
        except:
            raise

        return fname

    @abstractmethod
    def saveH5(self, fname: str, openpmd: bool = True):
        """Save the simulation data to hdf5 file.

        :param fname: The filename (path) of the file to write the data to.
        :type  fname: str

        :param openpmd: Flag that controls whether the data is to be written in according to the openpmd metadata standard. Default is True.

        """

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, val):
        raise AttributeError("Attribute 'data' is read-only.")

    @abstractmethod
    def backengine(self):
        pass

    @classmethod
    def run_from_cli(cls):
        """
        Method to start calculator computations from command line.

        :return: exit with status code

        """
        if len(sys.argv) == 2:
            fname = sys.argv[1]
            calculator = cls(fname)
            status = calculator._run()
            sys.exit(status)

    def _run(self):
        """
        Method to do computations. By default starts backengine.

        :return: status code.

        """
        result = self.backengine()

        if result is None:
            result = 0

        return result

    def _set_data(self, data):
        """ """
        """ Private method to store the data on the object.

        :param data: The data to store.

        """

        self.__data = data


# This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 823852.
