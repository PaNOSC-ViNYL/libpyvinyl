# libpyvinyl - The python APIs for Virtual Neutron and x-raY Laboratory

[![CI](https://github.com/PaNOSC-ViNYL/libpyvinyl/actions/workflows/ci.yml/badge.svg)](https://github.com/PaNOSC-ViNYL/libpyvinyl/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/libpyvinyl/badge/?version=latest)](https://libpyvinyl.readthedocs.io/en/latest/?badge=latest)

## Summary

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
The anticipated use is to inherit specialised `Calculators` from `BaseCalculator` and to
implement the core functionality in the derived class. In particular, this is required
for the methods responsible to launch a simulation through the `backengine()` method.

As an example, we demonstrate in an [accompanying notebook](https://github.com/PaNOSC-ViNYL/libpyvinyl/blob/master/doc/source/include/notebooks/example-01.ipynb)
how to declare a derived `Calculator` and implement a `backengine` method. The example then
shows how to run the simulation, store the results in a `hdf5` file, snapshot the simulation
and reload the simulation into memory.

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

### Developers

We provide a requirements file for developers in _requirements/dev.txt_.

```
$> cd requirements
$> pip install -r dev.txt
```

`conda install` is currently not supported.

Then, install `libpyvinyl` into the same environment. The `-e` flag links the installed library to
the source code in the repository, such that changes in the latter are immediately effective in the installed version.

```
$> cd ..
$> pip install -e .
```

## Testing

We recommend to run the unittests and integration tests.

```
$> pytest tests
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

## Acknowledgement

This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 823852.
