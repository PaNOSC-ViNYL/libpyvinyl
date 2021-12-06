"""
The following documents how the various classes in libpyvinyl and a IO class to be implemented
are supposed to be used.
"""

from IO import OpenPMD
import InteractionCalculator, DiffractionCalculator, ...

interaction = InteractionCalculator()
interaction.input = OpenPMD('prop.h5') # Load data from native Progapator output into openpmd format that interaction can digest.
interaction.output = 'pmi.h5' # Specify filename, will be passed down to backengine.

diffraction = DiffractionCalculator()
diffraction.input = OpenPMD(interaction.output) # Load native pmi output as openpmd so diffraction can digest.
diffraction.output = "diffraction.nexus" # Set filename, will be passed down to diffraction backengine.

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

# Run the simulation of a whole instrument.
spb.run()

OpenPMD(diffraction.output, instrument=instrument).dump("spb.nexus")


