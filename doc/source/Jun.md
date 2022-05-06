## Quickstart

This is the quickstart guide for creating a simulation workflow package based on `libpyvinyl`. Please
first install `libpyvinyl` following the instruction in the `Installation` section.

### Design a minimal instrument
As a minimal start, we will create an instrument with a calculator that can get the sum of two numbers.

There are 3 specialized classes needed to be defined for the package:
- `CalculatorClass`: a class based on `BaseCalculator` to perform the calculation.
- `DataClass`: to represent the input and output data of the `CalculatorClass`.
- `FormatClass`: the interface to exchange data between the memory and the file on the disk in a specific format.

### Define a DataClass
Let's firstly define a `NumberData` class mapping the python objects in the memory. This is done by creating a mapping
dictionary to connect the data (e.g. an array or a single value) in the python object to the reference variable.

```py
from libpyvinyl.BaseData import BaseData

class NumberData(BaseData):
    def __init__(
        self,
        key,
        data_dict=None,
        filename=None,
        file_format_class=None,
        file_format_kwargs=None,
    ):

        expected_data = {}

        ### DataClass developer's job start
        expected_data["number"] = None
        ### DataClass developer's job end

        super().__init__(
            key,
            expected_data,
            data_dict,
            filename,
            file_format_class,
            file_format_kwargs,
        )

    @classmethod
    def supported_formats(self):
        ### DataClass developer's job start
        format_dict = self._dict_python_object()
        ### DataClass developer's job end
        return format_dict
```
The above example shows a minimal definition of an abstract class.

we define the `expected_data` dictionary for the `NumberData` class.

### Define two CalculatorClasses
$$ 

#### Define the default CalculatorParameters

#### Define the input and output

#### Define backengine

#### Define an instrument

...

### Run the instrument