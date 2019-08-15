# Apache License 2.0
# 
# Copyright (c) 2010-2019 Gurpreet Anand (http://gurpreetanand.com)
#
# See README.md and LICENSE for details.
#
# Author: Gurpreet Singh Anand
# Email: gurpreetsinghanand@live.com
# Project Repository: https://github.com/GurpreetSinghAnand/noipyd/noipyd/core
# Filename: parser.py
# Description:

from .base import BaseParser
from .response import JSONResponse


class DOMParser(BaseParser):
    from bs4 import BeautifulSoup

    def __init__(self, **kwargs):
        super(DOMParser, self).__init__(**kwargs)

        self.document = None
        self.target = None

        self.set(**kwargs)

    def __set_document__(self, document):
        self.document = self.BeautifulSoup(str(document), 'html.parser')

    def __get_document__(self):
        return self.document

    def __set_target__(self, target):
        self.target = target

    def __get_target__(self):
        return self.target

    def parse(self):
        return self.document.select(self.__get_target__())


class DomainParser(BaseParser):

    def __init__(self, **kwargs):
        super(DomainParser, self).__init__(**kwargs)

        self.dom = None
        self.domains = []
        self.rows = []

        self._content = 'table.table-stack tbody tr'
        self._target = 'td:first-child span'
        # self._target = 'td'

        self.set(**kwargs)

    def __set_dom__(self, dom):
        self.dom = dom

    def __get_dom__(self):
        return self.dom

    def __set_domains__(self, domains):
        self.domains = domains.copy()

    def __get_domains__(self):
        return self.domains

    def __set_rows__(self, rows):
        self.rows = rows.copy()

    def __get_rows__(self):
        return self.rows

    def parse(self):
        domains = []
        parser = DOMParser(document=self.__get_dom__(), target=self._content, special_properties=['document'])
        content = parser.parse()
        self.__set_rows__(content)
        for row in self.__get_rows__():
            row = parser.BeautifulSoup(str(row), 'html.parser')
            for target in row.select(self._target):
                target = parser.BeautifulSoup(str(target), 'html.parser')
                domains.append(target.get_text().strip())
        self.__set_domains__(domains)
        print(self.__get_domains__())



