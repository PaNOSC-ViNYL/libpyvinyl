#! /usr/bin/env python3
"""
:module Test: Top level test module hosting all unittest suites.
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

import unittest
import os, sys

from BaseCalculatorTest import BaseCalculatorTest
from DetectorTest import DetectorTest
from RadiationSampleInteractorTest import RadiationSampleInteractorTest
from BeamlinePropagatorTest import BeamlinePropagatorTest, BeamlinePropagatorParametersTest
from SignalGeneratorTest import SignalGeneratorTest
from ParametersTest import Test_Parameter, Test_Parameters, Test_Instruments

# Are we running on CI server?
is_travisCI = ("TRAVIS_BUILD_DIR" in list(
    os.environ.keys())) and (os.environ["TRAVIS_BUILD_DIR"] != "")


def suite():
    suites = [
        unittest.makeSuite(BaseCalculatorTest, 'test'),
        unittest.makeSuite(DetectorTest, 'test'),
        unittest.makeSuite(RadiationSampleInteractorTest, 'test'),
        unittest.makeSuite(BeamlinePropagatorTest, 'test'),
        unittest.makeSuite(BeamlinePropagatorParametersTest, 'test'),
        unittest.makeSuite(SignalGeneratorTest, 'test'),
        unittest.makeSuite(Test_Parameter, 'test'),
        unittest.makeSuite(Test_Parameters, 'test'),
        unittest.makeSuite(Test_Instruments, 'test'),
    ]

    return unittest.TestSuite(suites)


# Run the suite and return a success status code. This enables running an automated git-bisect.
if __name__ == "__main__":

    result = unittest.TextTestRunner(verbosity=2).run(suite())

    if result.wasSuccessful():
        print('---> OK <---')
        sys.exit(0)

    sys.exit(1)
