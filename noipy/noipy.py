#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Apache License 2.0
#
# Copyright (c) 2010-2019 Gurpreet Anand (http://gurpreetanand.com)
#
# See README.rst and LICENSE for details.
#
# Author: Gurpreet Singh Anand
# Email: gurpreetsinghanand@live.com
# Project Repository: https://github.com/GurpreetSinghAnand/noipy/noipy/
# Filename: noipy.py
# Description:

import argparse
from core.agent import NoIPWebAgent

__version__ = '1.0.1'

def  main():
    parser = argparse.ArgumentParser(prog='noipy', description='A utility tool to automate NO-IP domain renewal')
    parser.add_argument("-u", "--username",
                        required=True,
                        help="the NoIP USERNAME",
                        dest="username",
                        metavar="USERNAME")
    parser.add_argument("-p", "--password",
                        required=True,
                        help="the NoIP PASSWORD",
                        dest="password",
                        metavar="PASSWORD")
    parser.add_argument("-d", "--domain",
                        required=True,
                        help="the NoIP DOMAIN",
                        dest="domain",
                        metavar="DOMAIN")


    args = parser.parse_args()
    kwargs = vars(args)
    agent = NoIPWebAgent(**kwargs)