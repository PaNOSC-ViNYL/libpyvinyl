import numpy
from libpyvinyl.BaseCalculator import BaseCalculator
from libpyvinyl.Parameters import CalculatorParameters, InstrumentParameters

# Mocks for testing. Have to be here to work around bug in dill that does not
# like classes to be defined outside of __main__.
class SpecializedCalculator(BaseCalculator):
    def __init__(self, name, parameters=None, dumpfile=None, **kwargs):

        super().__init__(name, parameters, dumpfile, **kwargs)

    def setParams(self, photon_energy: float = 10, pulse_energy: float = 1e-3):
        if not isinstance(self.parameters, CalculatorParameters):
            self.parameters = CalculatorParameters()
        self.parameters.new_parameter(
            "photon_energy", unit="eV", comment="Photon energy"
        )
        self.parameters["photon_energy"].value = photon_energy

        self.parameters.new_parameter(
            "pulse_energy", unit="joule", comment="Pulse energy"
        )
        self.parameters["pulse_energy"].value = pulse_energy

    def backengine(self):
        self._BaseCalculator__data = numpy.random.normal(
            loc=self.parameters["photon_energy"].value,
            scale=0.001 * self.parameters["photon_energy"].value,
            size=(100,),
        )

        return 0

    def saveH5(self, openpmd=False):
        with h5py.File(self.output_path, "w") as h5:
            ds = h5.create_dataset("/data", data=self.data)

            h5.close()
