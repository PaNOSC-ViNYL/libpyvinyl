from setuptools import setup
import sys

requirements = ["pint",
                "dill",
                "numpy",
                "scipy",
                "jsons",
                "h5py",
                ]

setup(
  name='libpyvinyl',
  packages=['libpyvinyl'],
  version='0.0.2',
  license='LGPLv3',
  description='The python API for photon and neutron simulation codes in the Photon and Neutron Open Science Cloud (PaNOSC).',
  author='Carsten Fortmann-Grote',
  author_email='carsten.grote@xfel.eu',
  url='https://github.com/PaNOSC-ViNYL/libpyvinyl',
  download_url='https://github.com/PaNOSC-ViNYL/libpyvinyl/archive/v0.0.1.tar.gz',
  keywords=['photons', 'neutrons', 'simulations'],
  install_requires=requirements,
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
) 
