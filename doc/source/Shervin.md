## Instrument
libpyvinyl provides the `Instrument` class as a high level API to manage the full simulation of an entire instrument at a neutron or x-ray facility from the source, through the beamline propagation, the interaction with the sample under investigation and the detection from the detectors.

An instrument class is a convenience class, collecting in a sequence one or more calculators and their parameters in order to have an effective I/O chain from one calculator to the following till the end of the simulation.



### How to use an instrument

The user of the instrument is supposed to have an instantiated instrument object somehow.

The user is supposed to know the list of parameters that he can modify doing:
`mymasters = myinstrument.master`
where `mymasters` is of type MasterParameters (a collection of master parameters).

The list of calculators can be queried and printed on screen with the `list_calculators` methd.
The list of parameters can be queried and printed on screen via the `list_parameters` method.


### How to write an instrument

Firstly an instrument object has to be constructed with a name and the base path where the output of the calculators forming the instrument should go.

Optionally the list of calculators can be added afterwards or given at construction as a list of calculators.

Calculators should be added one by one with the `add_calculator` method providing an already instantiated calculator with its parameters.

At this stage is good practice to split parameters into two categories:
  1. parameters used by a calculator, defined for the specific instrument, but to supposed to be changed at runtime by the user running the simulation. 
	E.g. the parameter defining the distance between the sample and the detectors
  1. parameters supposed to be changed by the user running the simulation for the instrument
    E.g. wavelength of the neutrons 
	These usually match the list of the instrument parameters that are set during the data acquisition at the facility, experiment by experiment.
	To this category belong also parameters that are shared between different calculators.
	They might have different values for the different calculators, but have the same value and whenever they are changed, the value should be changed for all the calculators of the instrument.

Parameters that fall in the first category are set when declaring the calculator.

Parameters of the second category are called "master parameters" and should be added to the instrument with the `add_master_parameter` method.
It requires in input a convenience name, used to refer to the parameter and a dictionary.
  
The dictionary associates the name of a parameter and the calculator in which it is defined.

The user running the simulation will access only to master parameters.
    


