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


def main():
    parser = argparse.ArgumentParser(prog='noipy', description='A utility tool to automate NO-IP domain renewal')
    parser.add_argument("-u", "--username",
                        required=True,
                        help="The NoIP USERNAME",
                        dest="username",
                        metavar="USERNAME")
    parser.add_argument("-p", "--password",
                        required=True,
                        help="The NoIP PASSWORD",
                        dest="password",
                        metavar="PASSWORD")
    parser.add_argument("-r", "--register",
                        required=False,
                        default=False,
                        action='store_true',
                        help="Save NoIP credentials in database",
                        dest="must_register")
    parser.add_argument("-w", "--workers",
                        required=True,
                        help="Number of WORKERS to run concurrently",
                        dest="workers",
                        metavar="WORKERS")
    parser.add_argument("-l", "--log-level",
                        required=False,
                        help="LOG LEVEL for saving logs",
                        dest="log_level",
                        metavar="LOG LEVEL")
    parser.add_argument("-f", "--log-file",
                        required=False,
                        help="LOG FILE to save logs",
                        dest="log_file",
                        metavar="LOG FILE")


    args = parser.parse_args()
    kwargs = vars(args)
    agent = NoIPWebAgent(**kwargs)