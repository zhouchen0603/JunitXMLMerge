"""This file defines how helmut is installed in a python environment.
Please review to the README.md's Installation section on "Using
setup.py".
"""
import setuptools
from junit_report_merge import __version__

setuptools.setup(
    name='JunitXMLMerge',
    version=__version__,
    packages=setuptools.find_packages(),
    author='zora zhou',
    author_email='zzhou@splunk.com',
    url='https://0.0.0.0:22',
    install_requires=['junitparser', 'pytest-rerunfailures'],
    test_suite='test',
    scripts = ['bin/JunitXMLMerge']
)
