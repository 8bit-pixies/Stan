from __future__ import print_function
from setuptools import setup, find_packages

#import sandman
import stan

long_description = read('README.md')

MAJOR = 0
MINOR = 0
MICRO = 1
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)


setup(
    name='stan',
    version=VERSION,
    url='http://github.com/chappers/stan/',
    license='MIT',
    author='Chapman Siu',
    author_email='chapm0n.siu@gmail.com',
    install_requires=['pandas>=0.12.0',
                      'pyparsing>=2.0.0'
                    ],    
    description='Statistical Analysis System Transcompiler to Python',
    long_description=long_description,
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
)