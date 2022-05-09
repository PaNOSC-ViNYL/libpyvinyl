# User guide

## BaseCalculator
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

### In the __init__ method
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

### Define the CalculatorParameters
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

### Define the backengine

There are several variables should be used in the `backeigine()`:
- `self.input`: A `DataCollection` containing `input` data. `self.input.to_list()[0].get_data()` can get the first input data.
- `self.output`: This initialized variable should be mapped to either a python dictionary or a file by either `set_dict()` or
`set_file()`. For example:
```py
    key = self.output_keys[0]
    output_data = self.output[key]
    output_data.set_dict(data_dict)
```

### Dump the object
The finial users can use`dump()` and `from_dump()` to snapshot/restore a Calculator object.
No modification needed when you create a derived class.

## Data API
`libpyvinyl` provides several abstract classes to create data interfaces.

### DataCollection
`DataCollection` is a thin layer interface between the Calculator and DataClass. It aggregates
the input and output into a single variable, respectively.

A `DataCollection` can be initialized with several DataClass instances like this:
```py
collection = DataCollection(data_1, data_2, ..., data_n)
```
or with the `add_data()`:
```py
collection = DataCollection()
collection.add_data(data_1, data_2, ..., data_n)
```

A data can be accessed by its key:
```py
data_1 = collection["data_1_key"]
```

A list of data dictionaries of the data in a `DataCollection` can be obtained:
```py
collection.get_data()
```

You can also create a list of the Data objects in the `DataCollection`
```py
collection.to_list()
```

To get an overview of the `DataCollection`, just print it out:
```
print(collection)
```
### BaseData
A specialized Data class can be created for a kind of data with similar attributes
based on the abstract `BaseData` class. The abstract class provides useful helper
functions and a template for the Data interface.

A file-mapping DataClass will not read the file until the final user calls `get_data()`, which
calls the `read()` method of its `file_format_class` and returns
the python dictionary of the data. The `file_format_class` is defined by one of these functions:

To create/set a DataClass as a python dictionary mapping:
- `from_dict()`: Create a class instance mapping from a python dictionary.
- `set_dict()`: Set the class as a python dictionary mapping.

To create/set a DataClass as a file mapping:
- `set_file()`: Set the class as a file mapping.
- `from_file()`: Create a class instance mapping from a file.

To write the Data class into a file in a certain file format you can:
```py
data_file = data.write(filename = 'test_file', format_class=FormatClass)
```
The file can then be written into a `test_file`, with the FormatClass you specify.

To list the formats supported by the Data Class:
- `list_formats()`: This method prints the return of `supported_formats()`, which needs
to be defined for the derived class.

#### Develop a derived DataClass
A DataClass derived from the `BaseData` class only needs two pieces of information:
- `expected_data`: a dictionary whose key defines the data needed.
- `supported_formats()`, it returns a dictionary describing the supported formats.
The information is extracted from the format class with the `_add_ioformat()` method.
An example:

```py
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
        format_dict = {}
        ### DataClass developer's job start
        self._add_ioformat(format_dict, TXTFormat.TXTFormat)
        self._add_ioformat(format_dict, H5Format.H5Format)
        ### DataClass developer's job end
        return format_dict
```

### BaseFormat
The Format class is the interface between the exact file and
the python object.

For each derived FormatClass, we have to provide the content of:
- `format_register()`: to provide the meta data of this format.
- `read()`: how do we read the file into a python dictionary, whose
keys must include the keys of the `expected_data` of the DataClass connecting to
this format.
- `write()`: how do we write the data of the DataClass into a file in this format.

Optionally, a direct convert method can be defined to avoid reading the whole
data into the memory. See:
- BaseFormat.direct_convert_formats()
- BaseFormat.convert()

#### read() and write()
The `read()` method needs to return a python dictionary required by its corresponding
Data Class. Example:
```py
class NumberData(BaseData):
    ...
    expected_data = {}

    ### DataClass developer's job start
    expected_data["number"] = None
    ...


class TXTFormat(BaseFormat):
    ...
    @classmethod
    def read(cls, filename: str) -> dict:
            """Read the data from the file with the `filename` to a dictionary. The dictionary will
            be used by its corresponding data class."""
            number = float(np.loadtxt(filename))
            data_dict = {"number": number}
            return data_dict
    ...
```
The `write()` method should call `object.get_data()`, where the `object` is an instance of the FormatClass's corresponding
DataClass, and write the data to the intended file. It is recommended to return a DataClass object mapping to the newly written
file.

```py
class TXTFormat(BaseFormat):
    ...
    @classmethod
    def write(cls, object: NumberData, filename: str, key: str = None):
        """Save the data with the `filename`."""
        data_dict = object.get_data()
        arr = np.array([data_dict["number"]])
        np.savetxt(filename, arr, fmt="%.3f")
        if key is None:
            original_key = object.key
            key = original_key + "_to_TXTFormat"
        return object.from_file(filename, cls, key)
    ...
```


#### Example of a FormatClass:
```py
class TXTFormat(BaseFormat):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def format_register(self):
        key = "TXT"
        desciption = "TXT format for NumberData"
        file_extension = ".txt"
        read_kwargs = [""]
        write_kwargs = [""]
        return self._create_format_register(
            key, desciption, file_extension, read_kwargs, write_kwargs
        )

    @staticmethod
    def direct_convert_formats():
        # Assume the format can be converted directly to the formats supported by these classes:
        # AFormat, BFormat
        # Redefine this `direct_convert_formats` for a concrete format class
        return []

    @classmethod
    def read(cls, filename: str) -> dict:
        """Read the data from the file with the `filename` to a dictionary. The dictionary will
        be used by its corresponding data class."""
        number = float(np.loadtxt(filename))
        data_dict = {"number": number}
        return data_dict

    @classmethod
    def write(cls, object: NumberData, filename: str, key: str = None):
        """Save the data with the `filename`."""
        data_dict = object.get_data()
        arr = np.array([data_dict["number"]])
        np.savetxt(filename, arr, fmt="%.3f")
        if key is None:
            original_key = object.key
            key = original_key + "_to_TXTFormat"
        return object.from_file(filename, cls, key)
```