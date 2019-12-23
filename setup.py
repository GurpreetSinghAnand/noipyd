# Apache License 2.0
# 
# Copyright (c) 2010-2019 Gurpreet Anand (http://gurpreetanand.com)
#
# See README.md and LICENSE for details.
#
# Author: Gurpreet Singh Anand
# Email: gurpreetsinghanand@live.com
# Project Repository: https://bitbucket.org/gurpreet-anand/noipy/src/master/noipy/
# Filename: setup.py
# Description: Setup for `say-greetings` package

from setuptools import setup, find_packages

long_description = 'A utility tool to automate NO-IP domain renewal'

setup(
    name='say-greetings',
    version='1.0.0',
    author='Gurpreet Anand',
    author_email='gurpreetsinghanand@live.com',
    url='',
    description='A utility tool to automate NO-IP domain renewal',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'noipy=noipy.noipy:main'
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    keywords='noipy python package gurpreetsinghanand Gurpreet Anand',
    zip_safe=False
)