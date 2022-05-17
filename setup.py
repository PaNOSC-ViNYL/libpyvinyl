from setuptools import setup, find_packages
import sys

with open("requirements/prod.txt") as requirements_file:
    require = requirements_file.read()
    requirements = require.split()

import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name="libpyvinyl",
    packages=find_packages(include=["libpyvinyl", "libpyvinyl.*"]),
    version=get_version("libpyvinyl/__init__.py"),
    license="LGPLv3",
    description="The python API for photon and neutron simulation codes in the Photon and Neutron Open Science Cloud (PaNOSC).",
    author="Carsten Fortmann-Grote, Juncheng E, Mads Bertelsen, Shervin Nourbakhsh",
    author_email="carsten.grote@xfel.eu, juncheng.e@xfel.eu, Mads.Bertelsen@ess.eu, nourbakhsh@ill.fr",
    url="https://github.com/PaNOSC-ViNYL/libpyvinyl",
    download_url="https://github.com/PaNOSC-ViNYL/libpyvinyl/archive/v1.1.1.tar.gz",
    keywords=["photons", "neutrons", "simulations"],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
