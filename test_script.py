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
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException

driver_path='/usr/local/bin/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)
driver.get('http://www.buser.com.br')
# m_wrapper = driver.find_element(By.XPATH, "//div[@class='m-wrapper']")
# driver.find_element(By.XPATH, "//button[contains(text(), 'Fechar')]")
# close_button = m_wrapper.find_element(By.XPATH, "//button[@aria-label='Fechar']")
# close_button.click()

input_origem = driver.find_element(By.ID, "origem")
input_origem.send_keys('Belo Horizonte')
input_origem.send_keys(Keys.ENTER)

input_destination = driver.find_element(By.ID, "destino")
input_destination.send_keys('Rio de Janeiro')
input_destination.send_keys(Keys.ENTER)
input_ida = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Ida"]')))

input_ida.click()

calendario = driver.find_element(By.CLASS_NAME,"ada-calendar")

data_desejada = calendario.find_element(By.XPATH,"//button[@data-testid='20']")
data_desejada.click()


def selecionar_data(driver, data):
    # Extrai o ano, mês e dia da data fornecida
    ano, mes, dia = map(int, data.split('-'))
    
    # Calcula a diferença em meses entre a data atual e a data desejada
    data_atual = datetime.now().date()
    data_desejada = datetime(ano, mes, dia).date()
    dif_meses = (data_desejada.year - data_atual.year) * 12 + (data_desejada.month - data_atual.month)
    
    # Localiza o botão para navegar para o próximo mês
    botao_proximo_mes = driver.find_element(By.CSS_SELECTOR, 'button[data-testid="next"]')

    # Clique no botão para navegar para o próximo mês até chegar ao mês desejado
    for _ in range(dif_meses):
        botao_proximo_mes.click()

    # Aguarda até que o calendário seja atualizado para o mês desejado
    
    # Localiza o botão correspondente ao dia desejado no calendário
    botao_dia = driver.find_element(By.XPATH, f'//button[@data-testid={dia}]')
    
    # Clique no botão do dia desejado
    botao_dia.click()
data = '2023-09-01'

botao_buscar = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Buscar"]')

# Clique no botão de busca
botao_buscar.click()
