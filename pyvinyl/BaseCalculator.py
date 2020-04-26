"""
:module BaseCalculator: Module hosting the BaseCalculator and BaseParameters
abstract classes.
"""


####################################################################################
#                                                                                  #
# This file is part of pyvinyl - The APIs for Virtual Neutron and x-raY            #
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

from pyvinyl.AbstractBaseClass import AbstractBaseClass
from abc import abstractmethod
import copy
from tempfile import mkstemp
import os
import dill
from numbers import Number
from numpy import ndarray
import json, jsons
from jsons import JsonSerializable

import logging
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.WARNING)
# from pyvinyl import PhysicalQuantity, Unit

# ACCEPTED_VALUE_TYPES=[
#         BaseParameters,
#         str,
#         Number,
#         ndarray,
#         ]
#         # PhysicalQuantity,


        
class BaseParameters(JsonSerializable, AbstractBaseClass):
    """
    :class BaseParameters: Base class to encapsulate all parametrizations of
    Calculators.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        """
        :param kwargs: (key, value) pairs of parameters.
        """

        # Update parameters with additionaly given arguments.
        for key, val in kwargs.items():
            self.__dict__[key] = val

    def __call__(self, **kwargs):
        """ The copy constructor
        :param kwargs: key-value pairs of parameters to change in the new
        instance.

        :return: A new parameters instance with optionally changed parameters.
        """

        new = copy.deepcopy(self)

        if kwargs is None:
            return new

        for key, val in kwargs.items():
            new.__dict__[key] = val

        return new
    
    @classmethod
    def from_json(self, fname:str, **kwargs):
        """ Initialize an instance from a json file. """
        with open(fname, 'r') as fp:
            instance = self.load(json.load(fp))
        
        return instance

    def to_json(self, fname : str):
        """ Save this parameters class to a human readable json file.
        :param fname: Write to this file.
        :type  fname: str
        """

        with open(fname, 'w') as fp:
            json.dump(self.dump(), fp)
        

class BaseCalculator(AbstractBaseClass):
    """
    :class BaseCalculator: Base class of all calculators.
    """

    @abstractmethod
    def __init__(self, parameters=None, dumpfile=None, **kwargs):
        """
        :param parameters: The parameters for this calculator.
        :type  parameters: BaseParameters
        
        :param dumpfile: If given, load a previously dumped (aka pickled)
        calculator. If both 'parameters' and 'dumpfile' are given, the dumpfile
        is loaded first and parameters are overwritten. 

        :param kwargs: (key, value) pairs of further arguments to the
        calculator, e.g input_path, output_path.
        """
        
        if parameters is None and dumpfile is None:
            raise AttributeError("At least one of 'parameters' or 'dumpfile' must be given.")

        if dumpfile is not None:
            self.__load_from_dump(dumpfile)

        if parameters is not None:
            self.parameters = parameters

        if "output_path" in kwargs.keys():
            self.output_path = kwargs['output_path']
    
    def __call__(self, parameters=None, **kwargs):
        """ The copy constructor
        :param parameters: The parameters for the new calculator.
        :type  parameters: BaseParameters

        :param kwargs: key-value pairs of parameters to change in the new
        instance.

        :return: A new parameters instance with optionally changed parameters.
        """

        new = copy.deepcopy(self)

        for key, val in kwargs.items():
            new.__dict__[key] = val

        if parameters is not None:
            new.parameters = parameters

        return new
    
    def __load_from_dump(self, dumpfile):
        """ """
        """ Load a dill dump and initialize self's internals."""

        with open(dumpfile, 'rb') as fhandle:
            try:
                tmp = dill.load(fhandle)
            except:
                raise IOError("Cannot load calculator from {}.".format(dumpfile)) 

        self.__dict__ = copy.deepcopy(tmp.__dict__)

        del tmp
      
    @property
    def parameters(self):
        """ The parameters of this calculator. """

        return self.__parameters

    @parameters.setter
    def parameters(self, val):

        if not isinstance(val, (type(None), BaseParameters)):
            raise TypeError("""Passed argument 'parameters' has wrong type.  Expected BaseParameters, found {}.""".format(type(val)))

        self.__parameters = val

    def dump(self, fname=None):
        """
        Dump class instance to file.

        :param fname: Path to file to dump.

        """

        if fname is None:
            _, fname = mkstemp(
                    #suffix="_dump.dill",
                    #prefix=self.__class__.__name__[-1],
                    dir=os.getcwd(),
                    )
        try:
            with open(fname, "wb") as file_handle:
                dill.dump(self, file_handle)
        except:
            raise
                # raise IOError("Cannot dump to file "+fname)

        return fname

# Mocks for testing. Have to be here to work around bug in dill that does not
# like classes to be defined outside of __main__.
class SpecializedParameters(BaseParameters):

    def __init__(
            self, 
            photon_energy:float,
            pulse_energy:float,
            **kwargs
            ):
        
        super().__init__(
                photon_energy=photon_energy,
                pulse_energy=pulse_energy,
                **kwargs,
                )
    
class SpecializedCalculator(BaseCalculator):
    def __init__(self, parameters=None, dumpfile=None, **kwargs):
        
        super().__init__(parameters, dumpfile, **kwargs)


#This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 823852.
