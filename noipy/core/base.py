# Apache License 2.0
# 
# Copyright (c) 2010-2019 Gurpreet Anand (http://gurpreetanand.com)
#
# See README.rst and LICENSE for details.
#
# Author: Gurpreet Singh Anand
# Email: gurpreetsinghanand@live.com
# Project Repository: https://github.com/GurpreetSinghAnand/noipd/noipd/core
# Filename: base.py
# Description:


class Base(object):

    def __init__(self, **kwargs):

        self.special_properties = ['special_properties']

        if 'special_properties' in kwargs:
            self.__set_special_properties__(kwargs['special_properties'])

        self.set(**kwargs)

    def __set_special_properties__(self, special_properties):
        self.special_properties.extend(special_properties)

    def __get_special_properties__(self):
        return list(set(self.special_properties))

    def set(self, **kwargs):
        if kwargs != {}:
            for arg, val in kwargs.items():
                if val is None:
                    continue
                elif arg in self.special_properties:
                    eval('self.__set_{arg}__({val})'.format(arg=arg, val=val))
                else:
                    eval('self.__set_{arg}__(\'{val}\')'.format(arg=arg, val=val))
        else:
            raise NotImplementedError


class BaseAgent(Base):

    def __init__(self, **kwargs):
        super(BaseAgent, self).__init__(**kwargs)

    def run(self):
        pass


class BaseLogger(Base):

    def __init__(self, **kwargs):
        super(BaseLogger, self).__init__(**kwargs)

    def log(self):
        pass


class BaseParser(Base):

    def __init__(self, **kwargs):
        super(BaseParser, self).__init__(**kwargs)

    def parse(self):
        pass


class BaseResponse(Base):

    def __init__(self, **kwargs):
        super(BaseResponse, self).__init__(**kwargs)

    def respond(self):
        pass

