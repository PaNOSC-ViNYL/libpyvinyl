# libpyvinyl - The python APIs for Virtual Neutron and x-raY Laboratory

[![CI](https://github.com/PaNOSC-ViNYL/libpyvinyl/actions/workflows/ci.yml/badge.svg)](https://github.com/PaNOSC-ViNYL/libpyvinyl/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/libpyvinyl/badge/?version=latest)](https://libpyvinyl.readthedocs.io/en/latest/?badge=latest)


## Overview
**Installation instructions** [here](INSTALL.md)

Simulations provide invaluable insights to plan (before) and
 understand (after) experiments at neutron and X-ray facilities. 
A wide set of libraries and programs is already available to simulate
 neutron and X-ray beams, propagate them through the beamlines,
 interact with the sample and get data acquired by detectors. 

The aim of _libpyvinyl_ is to provide a high level neutron and X-ray simulation API. 
With this harmonized user interface we achieve seamless
interoperability of individual simulations thereby facilitating the
concatenation of simulation steps into a simulation pipeline. 
The vast differences with respect to parameter
 names, unit conventions, configuration syntax, i.e. the user
 interface, is, hence, overcome creating a `libpyvinyl` compliant API
 for each simulation software. 

## Software specific APIs based on libpyvinyl
The python package `libpyvinyl` provides a way to harmonize the user interfaces of such simulation codes. It is an object oriented library; its classes define the user interface to simulation codes, simulation parameters and simulation data.

For a given simulation code, e.g. propagation of neutron or photon
beams through a beamline, a new class would have to be defined that
derives from the `libpyvinyl` classes. 
This derived class requires the implementation of certain methods
meant to configure a simulation, launch the simulation code, and
retrieve the output data.
Since the interplay between parametrization, execution, and IO is
already taken care of at the level of `libpyvinyl`'s base classes, the
effort to define a specialized interface (parameters, backengine and
data object) for a new simulation code is rather minimal. This structure
allows integrating simulation codes into simulation pipelines in the
above sense. 

## What the libpyvinyl API offers
This API offers a homogeneous interface to:

- Configure a simulation.
- Launch the simulation run.
- Collect the simulation output data.
- Construct a `Data` instance that represents the simulation output data.
- Snapshoot a simulation by dumping the object to disk.
- Reload a simulation run from disk and continue the run with optionally modified parameters.

## Who should use this library
Three kind of users are the target of this package:
 1. developers of packages based on libpyvinyl offering new calculators
   for simulations
 1. users wishing to run a simulation giving some inputs and retrieving
   the results
 1. research facility experts that what to implement detailed
   simulation of existing instruments at their facility or  willing to
   design new ones
 
The fundamental class is the `BaseCalculator` and its sister class `Parameters`.
While `Parameters` is a pure state engine, i.e. it's sole purpose is to encapsulate
the physical, numerical, and computational parameters of a simulation, the `BaseCalculator`
exposes the interface to

- Configure a simulation.
- Launch the simulation run.
- Collect the simulation output data.
- Construct a `Data` instance that represents the simulation output data.
- Snapshot a simulation by dumping the object to disk.
- Reload a simulation run from disk and continue the run with optionally modified parameters.

The `BaseCalculator` is an abstract base class, it shall not be instantiated as such.
The anticipated use is to inherit specialized `Calculators` from `BaseCalculator` and to
implement the core functionality in the derived class. In particular, this is required
for the methods responsible to launch a simulation through the `backengine()` method.

As an example, we demonstrate in an [accompanying notebook](https://github.com/PaNOSC-ViNYL/libpyvinyl/blob/master/doc/source/include/notebooks/example-01.ipynb)
how to declare a derived `Calculator` and implement a `backengine` method. The example then
shows how to run the simulation, store the results in a `hdf5` file, snapshot the simulation
and reload the simulation into memory.


## libpyvinyl projects
There are currently two projects based on libpyvinyl:
- McStatsScript: [https://github.com/PaNOSC-ViNYL/McStasScript](https://github.com/PaNOSC-ViNYL/McStasScript)
- SimEx-Lite:[https://github.com/PaNOSC-ViNYL/SimEx-Lite](https://github.com/PaNOSC-ViNYL/SimEx-Lite)


## Documentation
Documentation can be generated as follows using sphinx:
```
cd doc/
pip install requirements.txt
make html
```

## Acknowledgement

This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 823852.
