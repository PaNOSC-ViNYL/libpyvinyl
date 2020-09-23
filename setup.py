from setuptools import setup
import sys
with open('requirements.txt', 'r') as fp:
    requirements=fp.readlines()

requirements = [r[:-1] for r in requirements]


setup(
  name = 'libpyvinyl',         # How you named your package folder (MyLib)
  packages = ['libpyvinyl'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='LGPLv3',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'The python API for photon and neutron simulation codes in the Photon and Neutron Open Science Cloud (PaNOSC).',   # Give a short description about your library
  author = 'Carsten Fortmann-Grote',                   # Type in your name
  author_email = 'carsten.grote@xfel.eu',      # Type in your E-Mail
  url = 'https://github.com/PaNOSC-ViNYL/libpyvinyl',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/PaNOSC-ViNYL/libpyvinyl/archive/v0.0.1.tar.gz',    # I explain this later on
  keywords = ['photons', 'neutrons', 'simulations'],   # Keywords that define your package best
  install_requires=requirements,
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Intended Audience :: Science/Research',      # Define that your audience are developers
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
) 
