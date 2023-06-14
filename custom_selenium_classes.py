#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 16:29:36 2023

@author: vitor
"""

import re
import os
import time
import csv
import pdb
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException, StaleElementReferenceException

class CustomDriver:
    def __init__(self, driver):
        self.driver = driver
    
    def __getattr__(self, attr):
        orig_attr = getattr(self.driver, attr)
        if callable(orig_attr):
            def wrapped(*args, **kwargs):
                pdb.set_trace()
                try:
                    result = orig_attr(*args, **kwargs)
                    if isinstance(result, WebElement):
                        return CustomWebElement(result)
                    return result
                except (StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException):
                    # Ações para fechar o m-wrapper e continuar a execução do código
                    # por exemplo, clicar no botão de fechar
                    
                    # Exemplo de ação para fechar o m-wrapper
                    self.driver.find_element_by_xpath('//button[@aria-label="Fechar"]').click()
                    
                    # Tente chamar o método original novamente
                    return orig_attr(*args, **kwargs)
            return wrapped
        else:
            return orig_attr
        
class CustomWebElement(WebElement):
    def __getattribute__(self, attr):
        orig_attr = super().__getattribute__(attr)
        if callable(orig_attr):
            def wrapped(*args, **kwargs):
                try:
                    return orig_attr(*args, **kwargs)
                except (StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException):
                    # Ações para fechar o m-wrapper e continuar a execução do código
                    # por exemplo, clicar no botão de fechar
                    
                    # Exemplo de ação para fechar o m-wrapper
                    self.find_element_by_xpath('//button[@aria-label="Fechar"]').click()
                    
                    # Tente chamar o método original novamente
                    return orig_attr(*args, **kwargs)
            return wrapped
        else:
            return orig_attr