from setuptools import setup
from setuptools import find_packages
import os

setup(
    name='fs2012_flow_sensor',
    version='0.1.0',
    description='Library for controlling the fs2012 flow sensors',
    long_description=__doc__,
    author='Will Dickson',
    author_email='wbd@caltech',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
    install_requires=['pyserial', 'matplotlib'],
    packages=find_packages(exclude=['examples',]),
    scripts=['fs2012_flow_sensor/bin/flow_sensor_app', 'fs2012_flow_sensor/bin/flow_sensor_live_plot'],
)
