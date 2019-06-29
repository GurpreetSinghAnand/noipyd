# The MIT License
# 
# Copyright (c) 2010-2019 Gurpreet Anand (http://gurpreetanand.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# 
# Author: Gurpreet Singh Anand
# Email: gurpreetsinghanand@live.com
# Project Repository: https://github.com/GurpreetSinghAnand/turtle/turtle
# Filename: agent.py
# Description:

class NoIPAgent(object):
    from selenium import webdriver
    __URL__ = 'https://www.noip.com/login?ref_url=console'
    __DDNS_URL__ = 'https://my.noip.com/#!/dynamic-dns'

    __DEFAULT_CHROME_OPTIONS__ = ['--headless', '--no-sandbox']
    __DEFAULT_SERVICE_ARGS__ = ['--verbose', '--log-path=/tmp/chromedriver.log']

    __DOMAINS_CSS__ = 'tr.table-striped-row'
    __MODIFY_CONFIRM_BTN_CSS__ = '.btn-labeled'
    __DOMAIN_NAME_CSS__ = 'td.word-break-col a.text-info'

    def __init__(self, **kwargs):
        self.username = None
        self.password = None
        self.domain = None
        self.domains = None
        self.browser = None

        self._is_logged_in = False
        self._chrome_options = None
        self._service_args = None

        self.set(**kwargs)

        self.init_browser()
        self.navigate(self.__URL__)
        self.login()
        self.navigate(self.__DDNS_URL__)
        self.fetch_domains()
        self.check_domain_renewal()

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

    def __set_domains__(self, domains):
        self.domains = domains

    def __get_domains__(self):
        return self.domains

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

    def set(self, **kwargs):
        if kwargs != {}:
            for arg, val in kwargs.items():
                if val is None:
                    continue
                elif arg in []:
                    eval('self.__set_{arg}__({val})'.format(arg=arg, val=val))
                else:
                    eval('self.__set_{arg}__(\'{val}\')'.format(arg=arg, val=val))
        else:
            pass

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

    def fetch_domains(self):
        domains = self.__get_browser__().find_elements_by_css_selector(self.__DOMAINS_CSS__)
        self.__set_domains__(domains)

    def check_domain_renewal(self):
        domains = self.__get_domains__()
        for domain in domains:
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