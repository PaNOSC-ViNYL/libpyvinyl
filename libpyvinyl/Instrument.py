"""
:module Instrument: Module hosting the Detector and DetectorParameters
abstract classes.
"""

from Parameters.Collections import ParametersCollection
import tempfile
from git import Repo
from pathlib import Path

class Instrument():
    """An Instrument class"""
    def __init__(self, calculators):
        """An Instrument class.

        :param calculators: A list of Calculator objects.
        :type calculators: list
        """
        self.calculators = {}
        self.params = ParametersCollection()
        for calculator in calculators:
            self.calculators[calculator.name] = calculator
            self.params.add(calculator.name, calculator.param)

class repository():
    """Initiate the repository from a URL or local path"""
    def __init__(self,
                 url="https://github.com/PaNOSC-ViNYL/instrument_database.git",
                 local_path=None,
                 branch=None):
        """Initiate the repository from a URL or local path

        :param url: The remote git repository URL, defaults to the vinyl repo.
        :type url: str, optional
        :param local_path: The local git path storing the instrument params, defaults to None.
        :type local_path: str, optional
        :param branch: The branch name, defaults to None to use the default branch.
        :type branch: str, optional
        """
        if url is not None:
            self.url = url
            if local_path is None:
                tmp_dir = tempfile.TemporaryDirectory()
                self.local_path = tmp_dir.name
                self.__tmp_dir = tmp_dir
            else:
                self.local_path = local_path
            self.repo = Repo.clone_from(self.url,self.local_path)
        else:
            self.local_path = local_path
            self.repo = Repo(local_path)
        if branch is not None:
            self.repo.git.checkout(branch)

    def switch_branch(self, branch_name):
        self.repo.git.checkout(branch_name)

    def ls_files(self, path='.'):
        """List the files in the repo"""
        p = Path(self.local_path)
        this_p = p/path
        files = [x for x in this_p.glob('[a-z0-9A-Z]*')]
        print(str(this_p)+':')
        for file in files:
            print(str(file.relative_to(this_p)))

    def ls_instrument(self):
        # TODO: How to define the .json files?
        """Print the names of the available instruments"""
        pass
    def load(self, instrument, version="HEAD"):
        """Load an intrument from the repository"""
        pass
        # return instrument_obj
    def dump_instrument(self, outfile):
        """Save the instrument in .py format"""
        # TODO: How to unfold the collection of calculators?
        pass
    def save_parameters(self, outfile):
        """Print the parameters of the instrument in .json format"""
        pass

if __name__ == "__main__":
    # my_instrument, my_params = repository(my_url).load(my_instrument)
    pass
