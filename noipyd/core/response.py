# Apache License 2.0
# 
# Copyright (c) 2010-2019 Gurpreet Anand (http://gurpreetanand.com)
#
# See README.md and LICENSE for details.
#
# Author: Gurpreet Singh Anand
# Email: gurpreetsinghanand@live.com
# Project Repository: https://github.com/GurpreetSinghAnand/noipyd/noipyd/core
# Filename: response.py
# Description:

from .base import BaseResponse


class JSONResponse(BaseResponse):
    import json

