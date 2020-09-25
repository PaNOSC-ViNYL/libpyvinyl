# libpyvinyl - The python APIs for Virtual Neutron and x-raY Laboratory

[![Build Status](https://travis-ci.com/PaNOSC-ViNYL/libpyvinyl.svg?branch=master)](https://travis-ci.com/PaNOSC-ViNYL/libpyvinyl)
[![Documentation Status](https://readthedocs.org/projects/libpyvinyl/badge/?version=latest)](https://libpyvinyl.readthedocs.io/en/latest/?badge=latest)
      
## Summary
The python package `libpyvinyl` exposes the high level API for simulation codes under
the umbrella of the Virtual Neutron and x-raY Laboratory (ViNYL). 

The fundamental class is the `BaseCalculator` and its sister class `Parameters`.
While `Parameters` is a pure state engine, i.e. it's sole purpose is to encapsulate
the physical, numerical, and computational parameters of a simulation, the `BaseCalculator`
exposes the interface to 

- Configure a simulation (through the corresponding `Parameters` instance)
- Launch the simulation run
- Collect the simulation output data and make it queriable as a class attribute
- Snapshoot a simulation by dumping the object to disk (using the `dill` library).
- Reload a simulation run from disk and continue the run with optionally modified parameters.

The `BaseCalculaton` is an abstract base class, it shall not be instantiated as such.
The anticipated use is to inherit specialised `Calculators` from `BaseCalculator` and to
implement the core functionality in the derived class. In particular, this is required
for the methods responsible to launch a simulation (`run()`) .

As an example, we demonstrate in an [accompanying notebook](https://github.com/PaNOSC-ViNYL/libpyvinyl/blob/master/doc/source/include/notebooks/example-01.ipynb)
how to declare a derived `Calculator` and implement a `backengine` method. The example then
shows how to run the simulation, store the results in a `hdf5` file, snapshot the simulation 
and reload the simulation into memory.

## Acknowledgement
This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 823852.


