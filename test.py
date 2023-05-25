#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 10:59:52 2023

@author: vitor
"""

from selenium import webdriver
from bs4 import BeautifulSoup
#import pandas as pd

# Configurar o caminho para o driver do Selenium (exemplo usando o ChromeDriver)
driver_path = '/usr/local/bin/chromedriver'  # Substitua pelo caminho real do driver

# Criar uma instância do WebDriver
driver = webdriver.Chrome(executable_path=driver_path)

# Navegar para a página de vagas do Glassdoor
url = 'https://www.clickbus.com.br/onibus/belo-horizonte-mg-todos/sao-paulo-sp-todos'  # Substitua pelo URL real do Glassdoor
driver.get(url)

# Esperar até que as vagas sejam carregadas
driver.implicitly_wait(10)  # Aguardar até 10 segundos (pode ser ajustado conforme necessário)

# Extrair o conteúdo HTML da página
html = driver.page_source

# Criar o objeto BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

search_results = soup.find(attrs={"data-testid": "search-results"})

# Encontre todos os containers dentro do elemento search-results com o atributo data-testid="search-item-container"
containers = search_results.find_all(attrs={"data-testid": "search-item-container"})

import re
from datetime import datetime, timedelta
for container in containers:
    company_element = container.find(class_ = re.compile(r"\w*company"))
    company_name = company_element.get('data-content')
    price_element = container.find(class_ = re.compile(r"\w*price"))
    price_text = price_element.text
    price = float(
        price_text
        .replace('R$', '')
        .replace('\xa0', '')
        .replace(",", ".")
        )
    date_element = container.find(class_ = re.compile(r"\w*hour"))
    departure_element = date_element.find("time", class_="departure-time")
    departure_date_string = departure_element.get('data-date')    
    departure_date = datetime.strptime(departure_date_string, "%Y-%m-%d")
    # Obter o horário de partida
    departure_time = departure_element.text
    return_element = date_element.find("time", class_="return-time") 
    return_element_list = return_element.text.split('+')
    return_time = return_element_list[0]
    if len(return_element_list) > 1:
        plus_days = int(return_element_list[1][0])
    else:
        plus_days = 0
    return_date_unformated = departure_date + timedelta(days=plus_days)
    return_date = return_date_unformated.strftime("%Y-%m-%d")
    location_element = container.find(class_ = re.compile(r"\w*bus-station"))
    departure_location_element = location_element.find(class_ = 'station-departure')
    departure_location = departure_location_element.text
    arrival_location_element = location_element.find(class_ = 'station-arrival')
    arrival_location = arrival_location_element.text
    
    # Pré-compile as expressões regulares
company_regex = re.compile(r"\w*company")
price_regex = re.compile(r"\w*price")
hour_regex = re.compile(r"\w*hour")

for container in containers:
    # Encontre o elemento da empresa
    company_element = container.find(class_=company_regex)
    company_name = company_element.get('data-content')

    # Encontre o elemento do preço
    price_element = container.find(class_=price_regex)
    price_text = price_element.get_text(strip=True)
    price = float(price_text.replace('R$', '').replace('\xa0', '').replace(",", "."))

    # Encontre o elemento da hora
    date_element = container.find(class_=hour_regex)

    # Encontre o horário de partida
    departure_element = date_element.find("time", class_="departure-time")
    departure_date_string = departure_element.get('data-date')
    departure_date = datetime.strptime(departure_date_string, "%Y-%m-%d")
    departure_time = departure_element.get_text(strip=True)

    # Encontre o horário de retorno
    return_element = date_element.find("time", class_="return-time")
    return_element_list = return_element.get_text(strip=True).split('+')
    return_time = return_element_list[0]
    plus_days = int(return_element_list[1][0]) if len(return_element_list) > 1 else 0

    # Calcule a data de retorno
    return_date_unformatted = departure_date + timedelta(days=plus_days)
    return_date = return_date_unformatted.strftime("%Y-%m-%d")

    # Encontre o local de partida e chegada
    location_element = container.find(class_=re.compile(r"\w*bus-station"))
    departure_location_element = location_element.find(class_='station-departure')
    departure_location = departure_location_element.get_text(strip=True)
    arrival_location_element = location_element.find(class_='station-arrival')
    arrival_location = arrival_location_element.get_text(strip=True)
    print(
        company_name, price, departure_date, return_date, departure_location,
        arrival_location
        )



    

# Extrair o número usando expressão regular
numero_match = re.search(r"\+(\d+)", string_horario)
numero = numero_match.group(1) if numero_match else ""

    print(price)
    


# Criar uma lista para armazenar os dados das vagas
dados_vagas = []

# Iterar sobre as vagas encontradas e extrair as informações desejadas
for vaga in vagas:
    titulo = vaga.find('a', class_='jobLink').text
    empresa = vaga.find('a', class_='jobLink').get('href')
    localizacao = vaga.find('span', class_='loc').text

    # Adicionar as informações da vaga à lista de dados
    dados_vagas.append({'Título': titulo, 'Empresa': empresa, 'Localização': localizacao})


    
    
    
