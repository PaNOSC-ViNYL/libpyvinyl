## Instrument
libpyvinyl provides the `Instrument` class as a high level API to manage the full simulation of an entire instrument at a neutron or x-ray facility from the source, through the beamline propagation, the interaction with the sample under investigation and the detection from the detectors.

The `Instrument` class is a convenience class, collecting in a sequence one or more calculators and their parameters in order to have an effective I/O chain from one calculator to the following till the end of the simulation when the data can be retrieved and saved.

### Type of parameters for an instrument
A distinction between two type of parameters have been introduced in this library.

 1. **Parameter** (`Parameter` class):
	more details about it can be found in [Parameter](parameter.md).
	It essentially represent any kind of parameter that is needed by a calculator.
	Parameters belonging to a single calculator are collected in the CalculatorParameters as a member of the calculator.
 2. **MasterParameter** (`MasterParameter` class):
	each instrument should have a collection of master paramaters. They have two purposes:
	 - single calculator parameters that are meant to be changed at runtime by the user and not simply for the internal functioning of the calculator. Such calculator parameters are declared as master parameters in order to let the user running the simulation to know which are the parameters that he is supposed to change without altering the functioning of the instrument.
	   E.g. the angles of a three axis spectrometer or collimation
	 - parameters from multiple calculators that are supposed to have the same value and meaning: the wavelenght might be used by the calculator of the source and also by the calculator of the beamline to change some optics
	 
One significant advantage in defining and using **master parameters** is that the units used by the calculator and those for the final user might be decoupled.
Each calculator will have its own parameter with some units. The `pint` quantities used for physical values allow unit conversions in a transparent way for the end user if the values are assigned as a pint quantity. The master parameter can then be defined in the unit that is most convenient for the user for setting and getting values.


### How to write an instrument

Firstly an instrument object has to be constructed with a name and the base path where the output of the calculators forming the instrument should go.

Example:
```
myinstr = Instrument("D22_quick", instrument_base_dir=".")
```

Optionally the list of calculators can be added afterwards or given at construction as a list of calculators.

Calculators should be added one by one with the `add_calculator` method providing an already instantiated calculator with its parameters set.
Example:
```
calculator_1 = SpecializedCalculator(name="calc1")
calculator_1.add_parameter("par1",unit="meV")
myinstr.add_calculator(calculator_1)
```

Adding the calculator, all the parameters are automatically handled by the Instrument and accessed via the `myinstrument.parameters` method. 

Now that an instrument is fully described, it highly recommended to define the master parameters with the `add_master_parameter` method.
One master parameter is defined by conveniet name 
and a dictionary associating the name of the calculator and the name of the parameter for the specific calculator. It is worth noting that the parameters with the same meaning my be defined with different names by different calculators.
Once a master parameter is added, the user running the simulation for the instrument will not have to care about the details of the calculators forming the instrument.

Example:
```
myinstr.add_master_parameter("wavelength", {"calc_1": "par_1"}, unit="GeV")
myinstr.add_master_parameter("collimation", {"calc_1": "par_2"}, unit="meter")
myinstr.master["wavelength"] = 4.5 * ureg.keV
myinstr.master["collimation"] = 2 * ureg.meter
```

**The user running the simulation will access only to master parameters.**


### How to use an instrument

The user of the instrument is supposed to have an instantiated instrument object.

The user can get the list of parameters that he can modify by doing:
`mymasters = myinstrument.master`
where `mymasters` is of type MasterParameters (a collection of master parameters).
It is possible to loop over it to access the single `MasterParameter`s or print them: `print(mymasters)`.

The list of calculators can be queried and printed on screen with the `list_calculators` methd.
The list of parameters can be queried and printed on screen via the `list_parameters` method.

