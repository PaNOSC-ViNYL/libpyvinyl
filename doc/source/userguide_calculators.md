
### BaseCalculator
`BaseCalculator` is an abstract class to help the developers build their own specialized Calculator
within the `libpyvinyl` framework. It takes a collection of Data derived from `BaseData` as input
and output and executes the operations defined in the `backegine()` method. The behavior of the
specialized Calculator is controlled by the parameters initialized in the `init_parameters()` method.

When you develop a specialized Calculator, consider about:
- What kinds are the input and output data?
- What are the parameters controlling the behavior of the backengine? And what are their default
values and their limits?
- How should the backengine behave?
- How to install the dependencies of the backengine?

#### In the __init__ method
In the
```
__init__(self,
        name: str,
        input: Union[DataCollection, list, BaseData],
        output_keys: Union[list, str],
        output_data_types: Union[list, BaseData],
        output_filenames: Union[list, str, None] = None,
        instrument_base_dir: str = "./",
        calculator_base_dir: str = "BaseCalculator",
        parameters: CalculatorParameters = None,)
```
method, `self.parameters` is assigned by the input `parameters`. If the `parameters` is `None`,
`self.parameters` will be initialized by the `self.init_parameters()` method.

The `input` variable can be either a `DataCollection`, a list of DataClass or a single DataClass.
It will be converted and treated as a `DataCollection`. In the end.

The `output_keys` defines the keys of the data in the `output` DataCollection. It is suggested
to be used in the `self.backengine()` method.


The `output_data_types` defines the types the DataClass of the data in the `output` DataCollection.
If the output types are fixed in the `backengine()` method, it can be ignored in the derived class.
An example fixing the output_data_types to NumberData:
```py
class ExpCalculator(BaseCalculator):
    def __init__(
        self,
        name: str,
        input: Union[DataCollection, list, NumberData],
        output_keys: Union[list, str] = ["plus_result"],
        output_filenames: Union[list, str] = [],
        instrument_base_dir="./",
        calculator_base_dir="PlusCalculator",
        parameters=None,
    ):
    super().__init__(
            name,
            input,
            output_keys,
            output_data_types=[NumberData],
            output_filenames=output_filenames,
            instrument_base_dir=instrument_base_dir,
            calculator_base_dir=calculator_base_dir,
            parameters=parameters,
        )
```

The `output_filenames` defines the filenames of the data in the `output` DataCollection, if the data
is a file_mapping. If the data is a dict_mapping, then the variable can be ignored as well.

An empty output `DataCollection` container: `self.output` is created  in the `__init_output()` method, which is called
by the `__init__()` method. The data types and keys are taken from the `self.output_data_types` and `self.output_data_keys`
parameters.

`instrument_base_dir` and `calculator_base_dir` set the base path of the calculator:
```
instrument_base_dir/calculator_base_dir
```
If the calculator
is added to an `Instrument` class object, the `instrument_base_dir` will be modified by the object.

#### Define the CalculatorParameters
The definition of the parameters and their default values are set in the `init_parameters()`
method. An empty `CalculatorParameters` object is firstly created and then filled with parameters
needed. In the end, the object should be assigned to `self.parameters`. Example:
```py
class PlusCalculator(BaseCalculator):
    ...
    def init_parameters(self):
        parameters = CalculatorParameters()
        times = parameters.new_parameter(
            "plus_times", comment="How many times to do the plus"
        )
        times.value = 1
        self.parameters = parameters
    ...
```
The detailed `parameters` guide: link

#### Define the backengine

There are several variables should be used in the `backeigine()`:
- `self.input`: A `DataCollection` containing `input` data. `self.input.to_list()[0].get_data()` can get the first input data.
- `self.output`: This initialized variable should be mapped to either a python dictionary or a file by either `set_dict()` or
`set_file()`. For example:
```py
    key = self.output_keys[0]
    output_data = self.output[key]
    output_data.set_dict(data_dict)
```

#### Dump the object
The finial users can use`dump()` and `from_dump()` to snapshot/restore a Calculator object.
No modification needed when you create a derived class.

