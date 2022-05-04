# libpyvinyl - The python APIs for Virtual Neutron and x-raY Laboratory

[![CI](https://github.com/PaNOSC-ViNYL/libpyvinyl/actions/workflows/ci.yml/badge.svg)](https://github.com/PaNOSC-ViNYL/libpyvinyl/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/libpyvinyl/badge/?version=latest)](https://libpyvinyl.readthedocs.io/en/latest/?badge=latest)

## Overview

The python package `libpyvinyl` exposes the high level API for simulation codes under
the umbrella of the Virtual Neutron and x-raY Laboratory (ViNYL).

The fundamental class is the `BaseCalculator` and its sister class `Parameters`.
While `Parameters` is a pure state engine, i.e. it's sole purpose is to encapsulate
the physical, numerical, and computational parameters of a simulation, the `BaseCalculator`
exposes the interface to

- Configure a simulation.
- Launch the simulation run.
- Collect the simulation output data.
- Construct a `Data` instance that represents the simulation output data.
- Snapshoot a simulation by dumping the object to disk.
- Reload a simulation run from disk and continue the run with optionally modified parameters.

The `BaseCalculator` is an abstract base class, it shall not be instantiated as such.
The anticipated use is to inherit specialized `Calculators` from `BaseCalculator` and to
implement the core functionality in the derived class. In particular, this is required
for the methods responsible to launch a simulation through the `backengine()` method.

As an example, we demonstrate in an [accompanying notebook](https://github.com/PaNOSC-ViNYL/libpyvinyl/blob/master/doc/source/include/notebooks/example-01.ipynb)
how to declare a derived `Calculator` and implement a `backengine` method. The example then
shows how to run the simulation, store the results in a `hdf5` file, snapshot the simulation
and reload the simulation into memory.

## Problem statement
Simulating physical processes is a widespread method to investigate *in-silico* complex systems that
are inaccessible to analytical methods. The "Virtual Neutron and x-raY Laboratory" (ViNYL)
is an attempt to represent essential elements of neutron or x--ray photon beamline experiments through
software that simulates the radiation passing from the source through beamlines, interacting with a sample and finally being registered in a detection device. In some
cases, multiple simulations have be chained in a simulation pipeline, where each segment of the experiment is represented by a different piece
of software. Driving such a complex simulation can be an enormous task due to the vast differences 
with respect to parameter names, unit conventions, configuration syntax, i.e. the user interface. 

The python package `libpyvinyl` provides a way to harmonize the user interfaces of such simulation codes. It is an object oriented library; its classes define the user interface to simulation codes, simulation parameters, and simulation data.

For a given simulation code, e.g. propagation of neutron or photon beams through a beamline, a new class would have to be defined that derives from the
`libpyvinyl` classes. Implementing the methods meant to configure a simulation, launch the simulation code, and retrieve the output data. Since the
interplay between parametrization, execution, and IO is already taken care of at the level of `libpyvinyl`'s base classes, the effort to define a specialized interface (parameters, backengine and DataClass) for a new simulation code is rather minimal. This structure allows integrating simulation codes into simulation pipelines in the above sense.

## Installation

We recommend installation in a virtual environment, either `conda` or `pyenv`.

### Create a `conda` environment

```
$> conda create -n libpyvinyl
```

### Common users

```
$> pip install libpyvinyl
```

### Developers of libpyvinyl

We provide a requirements file for developers in _requirements/dev.txt_.

```
$> cd requirements
```

```
$> conda install --file dev.txt
```

**or**

```
$> pip install -r dev.txt
```


Then, install `libpyvinyl` into the same environment. The `-e` flag links the installed library to
the source code in the local path, such that changes in the latter are immediately effective in the installed version.

```
$> cd ..
$> pip install -e .
```

## Testing

A simple `pytest` command will run the unittests and integration tests.
```
pytest ./
```

You should see a test report similar to this:

```
=============================================================== test session starts ================================================================
platform linux -- Python 3.8.10, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /home/juncheng/Projects/libpyvinyl
collected 100 items

integration/plusminus/tests/test_ArrayCalculators.py .                                                                                       [  1%]
integration/plusminus/tests/test_Instrument.py .                                                                                             [  2%]
integration/plusminus/tests/test_NumberCalculators.py ...                                                                                    [  5%]
integration/plusminus/tests/test_NumberData.py ...........                                                                                   [ 16%]
unit/test_BaseCalculator.py ..........                                                                                                       [ 26%]
unit/test_BaseData.py ...........................                                                                                            [ 53%]
unit/test_Instrument.py .......                                                                                                              [ 60%]
unit/test_Parameters.py ........................................                                                                             [100%]

=============================================================== 100 passed in 0.56s ================================================================
```

You can also run unittests only:

```
pytest tests/unit
```

Or to run integration tests only:

```
pytest tests/integration
```

## libpyvinyl projects
- McStatsScript
- SimEx-Lite


## Overview of base classes
### BaseCalculator
The `BaseCalculator` is an abstract base class providing the interface to the computing code: `input` and `output` for the data flow, `CalculatorParameters` to 
, `backengine` to execute the code. The connection between different `Calculator`s is handled by `BaseData` class.
### CalculatorParameters

### Parameter
### BaseData
### BaseFormat
### Instrument

## Example
The subdirectory *test/integration/plusminus* contains a python package that illustrates how a specialized calculator (simulation interface class) can be defined by deriving from the appropriate `libpyvinyl` base classes.



## Acknowledgement

This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 823852.