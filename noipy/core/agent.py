# Apache License 2.0
#
# Copyright (c) 2010-2019 Gurpreet Anand (http://gurpreetanand.com)
#
# See README.rst and LICENSE for details.
#
# Author: Gurpreet Singh Anand
# Email: gurpreetsinghanand@live.com
# Project Repository: https://github.com/GurpreetSinghAnand/noipyd/noipyd/core
# Filename: agent.py
# Description:
import pytz
import time
from .base import BaseAgent
from .parser import DomainParser
from configparser import ConfigParser
from datetime import datetime

class NoIPAgent(BaseAgent):
    from selenium import webdriver
    __URL__ = 'https://www.noip.com/login?ref_url=console'
    __DDNS_URL__ = 'https://my.noip.com/#!/dynamic-dns'

    __DEFAULT_CHROME_OPTIONS__ = ['--headless', '--no-sandbox', '--disable-gpu']
    __DEFAULT_SERVICE_ARGS__ = ['--verbose', '--log-path=/tmp/chromedriver.log']

    __DOMAINS_CSS__ = 'tr.table-striped-row'
    __MODIFY_CONFIRM_BTN_CSS__ = '.btn-labeled'
    __DOMAIN_NAME_CSS__ = 'td.word-break-col a.text-info'

    def __init__(self, **kwargs):
        super(NoIPAgent, self).__init__(**kwargs)

        self.username = None
        self.password = None
        self.browser = None

        self._domains = None
        self._is_logged_in = False
        self._chrome_options = None
        self._service_args = None

        self.set(**kwargs)

    def __set_username__(self, username):
        self.username = username

    def __get_username__(self):
        return self.username

    def __set_password__(self, password):
        self.password = password

    def __get_password__(self):
        return self.password

    def __set_domains__(self, domains):
        self._domains = domains

    def __get_domains__(self):
        return self._domains.copy()

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

    def __renew_domain__(self, dom, domain):
        modify_confirm_btn_elem = dom.select(self.__MODIFY_CONFIRM_BTN_CSS__).pop()
        renew_btn = self.__get_browser__().find_element_by_css_selector('{}.{}'.format(modify_confirm_btn_elem.name, '.'.join(modify_confirm_btn_elem.attrs.get('class'))))
        update_hostname_btn = self.__get_browser__().find_element_by_css_selector('button.btn.btn-170.btn-flat.btn-success.btn-round-corners.pr-sm.ml-sm-30')
        name = dom.select(self.__DOMAIN_NAME_CSS__).pop()
        if domain.get('host') == name.text.strip():
            if 'Confirm' in modify_confirm_btn_elem.text.strip():
                renew_btn.click()
                time.sleep(0.5)
                update_hostname_btn.click()
                time.sleep(1)
            else:
                print('{domain} is not due to get renewed until {_date}.'.format(domain=domain.get('host'), _date=datetime.strftime(datetime.fromtimestamp(domain.get('expires')), '%d/%m/%Y')))

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

    def register(self, username, password):
        pass

    def logout(self):
        dropdown_btn = self.__get_browser__().find_element_by_id('user-email-container')
        dropdown_btn.click()
        time.sleep(0.25)
        logout_btn = self.__get_browser__().find_element_by_css_selector('li#user-email-container > ul > li.hidden-xs > a')
        logout_btn.click()
        time.sleep(2)
        self.__get_browser__().quit()

    @property
    def domains(self):
        self.navigate(self.__DDNS_URL__)
        self.__get_browser__().execute_script
        document = self.__get_browser__().page_source
        document = ''.join(document.splitlines())
        document = document.encode('utf-8')
        parser = DomainParser(dom=document, special_properties=['dom'])
        return parser.parse()

    def check_domain_renewal(self):
        domains = self.domains.copy()
        for domain in domains:
            due_date = datetime.fromtimestamp(domain.get('expires'))
            due_date = due_date.astimezone(tz=pytz.utc)
            now = datetime.now(tz=pytz.utc)
            days_to_renew = (due_date - now).days
            if days_to_renew < 7:
                domain['is_due_for_renew'] = True
            else:
                domain['is_due_for_renew'] = False
        self.__set_domains__(domains)

    def renew(self):
        domains = self.__get_domains__()
        for domain in domains:
            if domain.get('is_due_for_renew'):
                self.__renew_domain__(dom=domain.get('domain'), domain=domain)
            else:
                continue


    def begin(self):
        self.init_browser()
        self.navigate(self.__URL__)
        self.login()
        self.check_domain_renewal()
        self.renew()
        self.logout()