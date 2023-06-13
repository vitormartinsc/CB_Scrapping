#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 15:10:19 2023

@author: vitor
"""

import re
import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException

driver_path='/usr/local/bin/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)
driver.get('http://www.buser.com.br')
m_wrapper = driver.find_element(By.XPATH, "//div[@class='m-wrapper']")
driver.find_element(By.XPATH, "//button[contains(text(), 'Fechar')]")
close_button = m_wrapper.find_element(By.XPATH, "//button[@aria-label='Fechar']")
close_button.click()

