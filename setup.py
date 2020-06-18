'''
Setup file for BioSim INF200 June package.

To create a package, run

python setup.py sdist

in the directory containing this file.

To create a zip archive, run

python setup.py sdist --formats=zip

The package will be placed in directory dist.

To install from the package, unpack it, move into the unpacked directory and
run

python setup.py install          # default location
python setup.py install --user   # per-user default location

See also
    http://docs.python.org/distutils
    http://docs.python.org/install
    http://guide.python-distribute.org/creation.html

'''

__author__ = "Anja Stene, Student NMBU", "Ghazal Azadi, Student NMBU"
__email__ = "anja.stene@nmbu.no", "ghazal.azadi@nmbu.no"

from distutils.core import setup

import codecs
import os
import setuptools

def read_readme():
      here = os.path.abspath(os.path.dirname(__file__))
      with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
            long_description = f.read()
            return long_description

setup(
      name='BioSim inf200 June 2020',
      version='0.1',
      description='A project Simulating a fictive Island with Animals',
      long_description=read_readme(),
      author='Anja Stene, Ghazal Azadi',
      author_email='anja.stene@nmbu.no, ghazal.azadi@nmbu.no',
      requires=['numpy (>=1.6.1)',
                'matplotlib (>=1.1.0)',
                'pytest'],
      #packages=['biosim', 'examples', 'tests'],
      packages=setuptools.find_packages(),
      url='https://github.com/anja0102/BioSim_G04_Anja_Ghazal',
      scripts=['examples/rv_demo.py', 'examples/rv_demo.py'],
      license='MIT License',
      keywords='simulation Island',
      classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Topic :: Science :: multivariate processes and simulation',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6'],
      )