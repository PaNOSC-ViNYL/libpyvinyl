"""
:module Instrument: Module hosting the Detector and DetectorParameters
abstract classes.
"""

from Parameters.Collections import ParametersCollection
import tempfile

class Instrument():
    """An Instrument class"""
    def __init__(self, calculators):
        """An Instrument class[summary]

        :param calculators: A list of Calculator objects.
        :type calculators: list
        """
        self.calculators = {}
        self.params = ParametersCollection()
        for calculator in calculators:
            self.calculators[calculator.name] = calculator
            self.params.add(calculator.name, calculator.param)

class repository():
    """Initiate the repository from a URL or local repo"""
    def __init__(self, url, local_repo=False):
        self.url = url

    def ls_instrument():
        """Print the names of the available instruments"""
        pass
    def load(instrument, version="HEAD"):
        """Load an intrument from the repository"""
        return instrument_obj
    def dump_instrument(outfile):
        """Save the instrument in .py format"""
        # TODO: How to unfold the collection of calculators?

    def save_parameters(outfile):
        """Print the parameters of the instrument in .json format"""



if __name__ == "__main__":
    my_instrument, my_params = repository(my_url).load(my_instrument)

