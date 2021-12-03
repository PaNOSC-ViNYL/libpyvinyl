"""
The following documents how the various classes in libpyvinyl and a IO class to be implemented
are supposed to be used.
"""

# Import a `format` module responsible for IO
import openpmd_io as IO


# Instantiate the IO class
io = IO(instrument., parameters. ...)

# Parameters, Instruments
parameters = Parameters()
istrument = Instrument()

# Data instance is on the calculator.
calculator = Calculator()

calculator.run()

# Now calculator has a non-None data member.

# Do the IO
io.write(calculator.data)
