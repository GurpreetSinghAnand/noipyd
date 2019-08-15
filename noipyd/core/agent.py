# Apache License 2.0
#
# Copyright (c) 2010-2019 Gurpreet Anand (http://gurpreetanand.com)
#
# See README.md and LICENSE for details.
#
# Author: Gurpreet Singh Anand
# Email: gurpreetsinghanand@live.com
# Project Repository: https://github.com/GurpreetSinghAnand/noipyd/noipyd/core
# Filename: agent.py
# Description:
from .base import BaseAgent
from .parser import DomainParser

class NoIPAgent(BaseAgent):
    from selenium import webdriver
    __URL__ = 'https://www.noip.com/login?ref_url=console'
    __DDNS_URL__ = 'https://my.noip.com/#!/dynamic-dns'

    __DEFAULT_CHROME_OPTIONS__ = ['--headless', '--no-sandbox']
    __DEFAULT_SERVICE_ARGS__ = ['--verbose', '--log-path=/tmp/chromedriver.log']

    __DOMAINS_CSS__ = 'tr.table-striped-row'
    __MODIFY_CONFIRM_BTN_CSS__ = '.btn-labeled'
    __DOMAIN_NAME_CSS__ = 'td.word-break-col a.text-info'

    def __init__(self, **kwargs):
        super(NoIPAgent, self).__init__(**kwargs)

        self.username = None
        self.password = None
        self.domain = None
        self.browser = None

        self._is_logged_in = False
        self._chrome_options = None
        self._service_args = None

        self.set(**kwargs)

        self.init_browser()
        self.navigate(self.__URL__)
        self.login()
        self.domains()
        # self.check_domain_renewal()

    def __set_username__(self, username):
        self.username = username

    def __get_username__(self):
        return self.username

    def __set_password__(self, password):
        self.password = password

    def __get_password__(self):
        return self.password

    def __set_domain__(self, domain):
        self.domain = domain

    def __get_domain__(self):
        return self.domain

    def __set_chrome_options__(self, chrome_options=None):
        self._chrome_options = self.webdriver.ChromeOptions()
        if chrome_options is None:
            for option in self.__DEFAULT_CHROME_OPTIONS__:
                self._chrome_options.add_argument(option)
        else:
            for option in list(chrome_options):
                self._chrome_options.add_argument(option)

    def __get_chrome_options__(self):
        return self._chrome_options

    def __set_service_args__(self, service_args=None):
        if service_args is None:
            self._service_args = self.__DEFAULT_SERVICE_ARGS__.copy()
        else:
            self._service_args = service_args

    def __get_service_args__(self):
        return self._service_args

    def __set_browser__(self, browser):
        self.browser = browser

    def __get_browser__(self):
        return self.browser

    def __validate__(self):
        assert 'No-IP' in self.__get_browser__().title

    def init_browser(self):
        self.__set_chrome_options__()
        self.__set_service_args__()
        browser = self.webdriver.Chrome(service_args=self.__get_service_args__())
        self.__set_browser__(browser)

    def navigate(self, url):
        self.__get_browser__().get(url)
        self.__validate__()

    def login(self):
        # Enter Email
        email_input_elem = self.__get_browser__().find_element_by_name('username')  # Find the search box
        email_input_elem.send_keys(self.__get_username__())
        # Enter Password
        password_elem = self.__get_browser__().find_element_by_name('password')  # Find the search box
        password_elem.send_keys(self.__get_password__())
        log_in_btn_elem = self.__get_browser__().find_element_by_name('Login')
        log_in_btn_elem.click()

        self._is_logged_in = True

    # @property
    def domains(self):
        self.navigate(self.__DDNS_URL__)
        self.__get_browser__().execute_script
        document = self.__get_browser__().page_source
        document = ''.join(document.splitlines())
        document = document.encode('utf-8')
        parser = DomainParser(dom=document, special_properties=['dom'])
        parser.parse()

    def check_domain_renewal(self):
        for domain in self.domains.items():
            modify_confirm_btn_elem = domain.find_element_by_css_selector(self.__MODIFY_CONFIRM_BTN_CSS__)
            domain_name = domain.find_element_by_css_selector(self.__DOMAIN_NAME_CSS__).text
            if self.domain == domain_name:
                if 'Confirm' in modify_confirm_btn_elem.text:
                    modify_confirm_btn_elem.click()
                else:
                    print('{domain} is not due to get renewed.'.format(domain=self.domain))
                    self.__get_browser__().quit()
            else:
                continue