import unittest
import os, sys


import BaseCalculatorTest

# Are we running on CI server?
is_travisCI = ("TRAVIS_BUILD_DIR" in list(os.environ.keys())) and (os.environ["TRAVIS_BUILD_DIR"] != "")


def suite():
    suites = [
             unittest.makeSuite(BaseCalculatorTest,               'test'),
             unittest.makeSuite(DetectorTest.py,                  'test'),
             unittest.makeSuite(RadiationSampleInteractorTest.py, 'test'),
             unittest.makeSuite(BeamlinePropagatorTest.py,        'test'),
             unittest.makeSuite(SignalGeneratorTest.py,           'test'),

             ]

    return unittest.TestSuite(suites)

# Run the suite and return a success status code. This enables running an automated git-bisect.
if __name__=="__main__":

    result = unittest.TextTestRunner(verbosity=2).run(suite())

    if result.wasSuccessful():
        print('---> OK <---')
        sys.exit(0)

    sys.exit(1)
