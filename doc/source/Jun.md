## Quickstart

This is the quickstart guide for creating a simulation workflow package based on `libpyvinyl`.

### Design a minimal instrument
As a minimal start, we will create an instrument with a calculator that can get the sum of two numbers.

There are 3 specialized classes needed to be defined for the package:
- `CalculatorClass`: a class based on `BaseCalculator` to perform the calculation.
- `DataClass`: to represent the input and output data of the `CalculatorClass`.
- `FormatClass`: the interface to exchange data between the memory and the file on the disk in a specific format.

### Define a DataClass
Let's firstly define the `DataClass` mapping the `dict`

### Define two CalculatorClasses
$$ 

#### Define the default CalculatorParameters

#### Define the input and output

#### Define backengine

#### Define an instrument

...

### Run the instrument