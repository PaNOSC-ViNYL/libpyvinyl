"""
:module BeamlinePropagator: Module hosting the BeamlinePropagator and BeamlinePropagatorParameters
abstract classes.
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

from libpyvinyl.BaseCalculator import BaseCalculator, Parameters

class BeamlinePropagatorParameters(Parameters):
    def __init__(self, **kwargs):
        
        super().__init__(**kwargs)


class BeamlinePropagator(BaseCalculator):
    def __init__(self, parameters=None, dumpfile=None, **kwargs):
        
        super().__init__(parameters, dumpfile, **kwargs)

    def backengine(self):
        pass

    def saveH5(self, fname, openpmd=True):
        pass

# This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 823852.
