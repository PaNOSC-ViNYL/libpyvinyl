"""
The following documents how the various classes in libpyvinyl and a IO class to be implemented
are supposed to be used.
"""

import InteractionCalculator, DiffractionCalculator, DataCollection
import WavefrontData, SampleData



base_path = 'my_base'
interaction = InteractionCalculator()
interaction.base_path = base_path
interaction.input = DataCollection(WavefrontData.file('prop.h5',format='wpg'), SampleData.file('sample.pdb',format='pdb'))
interaction.output_suffix = 'interaction'
interaction.backengine()

diffraction = DiffractionCalculator()
diffraction.base_path = base_path
diffraction.input = interaction.output
diffraction.output_suffix = 'diffr'
diffraction.backengine()
# It will write the files with the suffix.
diffraction.output.write(format='nexus')

# Inside backengine()
class InteractionCalculator(BaseCalculator):
    def __set_base_path(self, name):
        return self.base_path+'name'
    def backengine(self):
        # Native input
        wavefront_fn = self.input[0].convert(self.__set_base_path('wavefront.native'),'interaction_native_wavefront')
        sample_fn = self.input[1].convert(self.__set_base_path('sample.native'),'interaction_native_sample')
        # This can be a DataCollection if there are multiple data objects
        interaction_data = run_simulation_kernel(wavefront_fn, sample_fn, self.parameters)
        # The final result from the calculator, it's a DiffrasctionData object
        self.output = interaction_data

class DiffractionCalculator(BaseCalculator):
    def __set_base_path(self, name):
        return self.base_path+'name'
    def backengine(self):
        # Native input
        wavefront_fn = self.input[0].convert(self.__set_base_path('wavefront.native'),'calculator_native_wavefront')
        sample_fn = self.input[1].convert(self.__set_base_path('sample.native'),'calculator_native_sample')
        # This can be a DataCollection if there are multiple data objects
        diffraction_data = run_simulation_kernel(wavefront_fn, sample_fn, self.parameters)
        # The final result from the calculator, it's a DiffrasctionData object
        self.output = diffraction_data

# Instantiate an instrument class.
spb = Instrument()

# Instantiate the calculators, the default parameters are initialized within the calculators.
source = GenesisCalculator()
propagation = WPGCalculator()
interaction = XMDYNCalculator()
diffraction = SKOPICalculator()
detector = DetectorCalculator()

# Add the different parts to the instrument class
spb.add(source)
spb.add(propagation)
spb.add(interaction)
spb.add(diffraction)
spb.add(detector)
spb.set_base_path('base_path')
# Run the simulation of a whole instrument.
spb.run()

# Inside spb.run()
for calculator in spb.calculators:
    calculator.backengine()
    # Write the default format in the calculator
    calculator.output.write()