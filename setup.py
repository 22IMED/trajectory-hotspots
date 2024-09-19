# setup.py

from setuptools import setup, find_packages

setup(
    name='trajectory-hotspots',
    version='0.1.0',
    description='A Python library to detect hotspots between two trajectories',
    author='Imed Eddine ZEROUAL',
    author_email='imededdinezeroual@gmail.com',
    url='https://github.com/22IMED/trajectory-hotspots',
    packages=find_packages(),
    install_requires=['geopy'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
