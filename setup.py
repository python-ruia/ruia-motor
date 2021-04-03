#!/usr/bin/env python
"""
 Created by howie.hu at 2018/9/22.
"""

import os

from setuptools import find_packages, setup


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


setup(
    name='ruia_motor',
    version='0.0.4',
    author='Howie Hu',
    description="ruia_motor - a Ruia plugin that uses the motor to store data",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author_email='xiaozizayang@gmail.com',
    install_requires=['motor', 'ruia>=0.8.0'],
    url="https://github.com/python-ruia/ruia-motor",
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    project_urls={
        'Documentation': 'https://github.com/python-ruia/ruia-motor',
        'Source': 'https://github.com/python-ruia/ruia-motor',
    }
)
