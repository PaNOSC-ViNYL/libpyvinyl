## Quick start for developers using libpyvinyl

### Introduction
This section is intended to help a developer understand how a new simulation package can use libpyvinyl as a foundation. It is important to understand that libpyvinyl provides base classes from which a developer inherits more specialised classes from, and the final class then both contains the new functionality and the basic capabilities. To make a new package, a developer would have to inherit from these baseclasses:
- BaseCalculator
- BaseData
- BaseDataFormat

**Calculator**

The specialised calculator that inherits from BaseCalculator is capable of performing a calculation of some sort. The calculation can depend on some data and input values for parameters specified when the calculator is built. The calculator can also return output data. The scope of a calculator is somewhat arbitrary, but the power of libpyvinyl comes from the ability to break a big calculation down into smaller parts of individual calculators. When using a calculator, it is easy for the user to understand a small number of parameters as there are less risks of ambiguity. A rich Parameter class is provided by libpyvinyl to create the necessary parameters in each calculator. When creating a parameter it is possible to set allowed intervals to avoid undefined behaviour. 

**Data**

To create a description of some data that can be either given to or returned from a calculator one starts with the BaseData class. This data could be for example a number of particle states.

**DataFormat**

Each Data class will have a number of supported DataFormat which are necessary in order to save the data to disk. Our particle data from before could be saved as a json, yaml or some compressed format, and each would need a DataFormat class that contains methods to read and write such data, and make it available to a corresponding Data class.

### First steps as a developer
To build a simulation package in this framework, think about what calculation need to be performed and what parameters are needed to describe it. Then divide this big calculation into calculators with a limited number of parameters and clear input and output data. For example a particle source, it would need parameters describing the properties of emitted particles and then return a Data object with a large number of particle states. Then a calculator describing a piece of optics might have parameters describing its geometry, and it could have particle states as both input and output. With these kinds of considerations it becomes clear what Calculators and Data classes should be written.

### Benefit of libpyvinyl
When a package uses libpyvinyl as a foundation, libpyvinyl can be used to write a simulation from a series of these calculators using the Instrument class. Here is an example of a series of calculators that form a simple instrument.

| Calculator    | Description       | Parameters                     | Input Data      | Output Data     |
|:--------------|:------------------|:------------------------------:|:---------------:|:---------------:|
| Source        | Emits particles   | size, divergence, energy       | None            | particle states |
| Monochromator | Crystal           | position, d_spacing, mosaicity | particle states | particle states |
| Monochromator | Crystal           | position, d_spacing, mosaicity | particle states | particle states |
| Sample        | Crystal sample    | position, d_spacing, mosaicity | particle states | particle states |
| Detector      | Particle detector | position, size, sensitivity    | particle states | counts in bins  |

This setup uses two monochromators, each with their own parameters. The user can set up a master parameter that control both, for example to ensure they have the same d_spacing. Running the instrument then corresponds to running each calculator in turn and providing the output of one to the next.


