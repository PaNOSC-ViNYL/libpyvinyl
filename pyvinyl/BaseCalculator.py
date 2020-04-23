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

class BaseParameters(AbstractBaseClass):
    """
    :class BaseParameters: Base class to encapsulate all parametrizations of
    Calculators.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs: (key, value) pairs of parameters.
        """


class BaseCalculator(AbstractBaseClass):
    """
    :class BaseCalculator: Base class of all calculators.
    """

    def __init__(self, parameters: BaseParameters, **kwargs):
        """
        :param parameters: The parameters for this calculator.
        :type  parameters: BaseParameters

        :param kwargs: (key, value) pairs of further arguments to the
        calculator, e.g input_path, output_path.
        """
        
        self.parameters = parameters

        if "output_path" in kwargs.keys():
            self.output_path = kwargs['output_path']
        
    @property
    def parameters(self):
        """ The parameters of this calculator. """

        return self.__parameters
    @parameters.setter
    def parameters(self, val):

        if not isinstance(val, BaseParameters):
            raise TypeError("""Passed argument 'parameters' has wrong type.
            Expected BaseParameters, found {}.""".format(type(val)))

        self.__parameters = val
           

#This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 823852.
