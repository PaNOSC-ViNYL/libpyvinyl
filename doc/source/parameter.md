## User guide

### Parameter
The Parameter class describes a single parameter intended to be an input for a calculator. A parameter is initialised by the calculator and subsequently made available to the user. A parameter can have a physical unit and limits on the allowed value in order to avoid unmeaningful input. It is considered good practice to add a comment to each parameter to briefly explain its purpose.

#### Basic use
Here basic use of the Parameter class is shown with a brief example.
```
energy_parameter = Parameter(name="energy", unit="meV", comment="Energy of emitted particles")
```
There are a number of useful things one can do with a parameter object, for example print it to see what is currently contained. To get or set the value, the *value* attribute is used directly and all checks are performed internally.
```
energy_parameter.value = 5.0
```
We defined the default unit to be meV, but since the object is aware of the unit, it is possible to provide in another energy unit using Pint.
```
import pint
ureg = pint.UnitRegistry()
energy_parameter.value = 5.0*ureg.eV
```
Now the *energy_parameter* has a value of 5000.0 meV.

#### Limits
Many parameters have natural limits that would appear natural to the person writing a calculator, but perhaps not to a user. To transfer this knowledge, the developer can include limits in the parameter to cause an error if the value is set outside. Limits come in to forms, either as intervals or as options.

##### Intervals
The first type of limit to discuss is the interval, which can be between two finite numbers or extend to infinity in either end. Multiple intervals can be specified. It is possible to declare the intervals as legal or illegal, but all added intervals have to be of the same type, so it is not possible to mix legal and illegal intervals. Below a legal interval is added to the energy parameter.
```
energy_parameter.add_interval(min_value=0.0, max_value=7000.0, intervals_are_legal=True)
```
In order to extend an interval to infinity, one provides None for either *min_value* or *max_value*.
```
energy_parameter.add_interval(min_value=8000.0, max_value=None, intervals_are_legal=True)
```
Now the energy_parameter is legal from 0 to 7000 meV and from 8000 meV to infinity.

##### Options
It is also possible to define whether single values are legal or not, this is called an option, and has the same rules regarding legal / illegal as an interval, meaning all options have to be either legal or illegal. Lets make it illegal to have an energy of 0 meV.

```
energy_parameter.add_option(0, options_are_legal=False)
```
It is possible to add several options with one call using a list. We could make a few arbitrary values illegal in this way:
```
energy_parameter.add_option([5, 10], options_are_legal=False)
```
Now values of 0 meV, 5 meV and 10 meV would cause an error, even when they are all contained in a legal interval, as both the intervals and options are checked whenever a value is set.

##### Obtaining limits
When printing a parameter the limits will be available in human readable format, but it is also possible to obtain them with these methods for use in for example a GUI application that want to provide a slider or dropdown menu describing the parameter.
```
energy_parameter.get_intervals() # Returns list of tuples with min / max
energy_parameter.get_intervals_are_legal() # Returns True or False
energy_parameter.get_options() # Returns list of values
energy_parameter.get_options_are_legal() # Returns True or False
```

##### Clearing limits
It is possible to clear limits, with the *clear_intervals* and *clear_options* methods, yet doing so is not recommended, especially if the purpose is to run a simulation with a parameter value outside of what is assumed by the calculated.

### CalculatorParameters
The CalculatorParameters class is a container for holding all the Parameter objects that pertain to a single Calculator. Each Calculator can have just a single container to organise all the parameters, and it provides the expected container features for convenience. A CalculatorParameters object can be made without any Parameters, but let us create a CalculatorParameters object using our existing Parameter.

```
my_parameters = CalculatorParameters(parameters=[energy_parameter])
```
More parameters can be added using the *add* method.
```
my_parameters.add(Parameter("energy_spread", unit="meV", comment="Standard deviation of particle energies"))
```
The main purpose of the CalculatorParameters object is convenience, so it is possible to access the elements directly.
```
my_parameters["energy"].value = 7.0
my_parameters["energy_spread"].value = 0.8
```
It is also possible to perform a loop over the contained parameters, here we check if intervals are legal on the contained parameters.
```
for par in my_parameters:
    print(par.get_intervals_are_legal())
```
