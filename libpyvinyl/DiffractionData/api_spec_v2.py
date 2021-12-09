"""
The following documents how the various classes in libpyvinyl and a IO class to be implemented
are supposed to be used.
"""

import os
import subprocess
import XmdynCalculator, DiffractionCalculator, DataCollection
from WavefrontData import WavefrontData, WpgWavefrontFormat
from SampleData import SampleData, XmdynSampleFormat
# Class naming convention? XMDYNInteractionFormat or XmdynInteractionFormat
from InteractionData import InteractionData, XmdynInteractionFormat

# Case 01: Run simulation with the calcualtor generating output files
base_path = 'my_base'
input = DataCollection(
    WavefrontData.file('prop.h5', format=WpgWavefrontFormat, key='wavefront'),
    SampleData.file('sample.pdb', format=XmdynSampleFormat, key='sample'))
# The suffix of the output files (if generated)
output_suffix = 'interaction/'
interaction = XmdynCalculator(name='interaction',
                              base_path=base_path,
                              input=input,
                              output_suffix=output_suffix)
interaction_ouput = interaction.backengine()

output_suffix = 'diffraction/'
diffraction = DiffractionCalculator(name='diffraction',
                                    base_path=base_path,
                                    input=interaction_ouput,
                                    output_suffix=output_suffix)
diffraction_output = diffraction.backengine()
# It will write the files with the suffix.
diffraction_output.write(format='nexus')



# Inside backengine()
class XmdynCalculator(BaseCalculator):
    # Should be in BaseCalculator
    def get_file_path(self, name):
        """To keep the file directory consistent within the calculator."""
        name = output_suffix + name
        os.path.join(self.base_path, name)

    # Should be in BaseCalculator
    def list_input_keys(self):
        for key in self.__expected_input_keys:
            print(key)

    def __run(self, wavefront_fn, sample_fn, parameters):
        native_output_fn = 'interaction.native'
        command_sequence = [
            'xmdyn', sample_fn, wavefront_fn, 'par1',
            str(parameters['par1'].value), 'output',
            self.get_file_path(native_output_fn)
        ]
        proc = subprocess.Popen(command_sequence, stdout=subprocess.PIPE)
        for line in iter(proc.stdout.readline, b''):
            print('>>> {}'.format(line.rstrip()))
        return InteractionData.from_file(native_output_fn,
                                    format=XmdynInteractionFormat,
                                    key='interaction')

    def backengine(self):
        # Native input
        wavefront_fn = self.input['wavefront'].write(
            self.get_file_path('wavefront.native'), WpgWavefrontFormat)
        sample_fn = self.input['sample'].write(
            self.get_file_path('sample.native'), XmdynSampleFormat)
        # This is a DataCollection if there are multiple data objects
        interaction_data = self.__run(wavefront_fn, sample_fn, self.parameters)
        # The final result from the calculator, it's a DiffrasctionData object
        self.output = interaction_data
        return self.output

    # Should be in BaseCalculator
    def write(self, **kwargs):
        return self.output.write(**kwargs)


class DiffractionCalculator(BaseCalculator):
    # Should be in BaseCalculator
    def get_file_path(self, name):
        name = output_suffix + name
        os.path.join(self.base_path, name)

    # Should be in BaseCalculator
    def list_input_keys(self):
        for key in self.__expected_input_keys:
            print(key)

    def backengine(self):
        # Native input
        interaction_fn = self.input['interaction'].write(
            self.get_file_path('sample.native'), XmdynInteractionFormat)
        # This is a DataCollection if there are multiple data objects
        diffraction_data = run_simulation_kernel(interaction_fn,
                                                 self.parameters)
        # The final result from the calculator, it's a DiffrasctionData object
        self.output = diffraction_data
        return self.output

    # Should be in BaseCalculator
    def write(self, **kwargs):
        return self.output.write(**kwargs)


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
    calculator.write()