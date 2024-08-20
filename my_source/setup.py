# setup.py

from setuptools import setup, find_packages

setup(
    name='my_source',
    version='0.1',
    description='A package for mathematical and fitting functions',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'numba',
    ],
    python_requires='>=3.6',
)
