import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class ClickBusScraper:
    # Atualizar o driver_path de acordo com o caminho local para o chromedriver
    def __init__(self, driver_path='/usr/local/bin/chromedriver'):
        self.driver_path = driver_path
        self.driver = None
        # Experessões regulares que serão úteis para encontrar elementos html mais tarde
        self.company_regex = re.compile(r"\w*company")
        self.price_regex = re.compile(r"\w*price")
        self.hour_regex = re.compile(r"\w*hour")
        
    def scrape(self, departure_location_list, arrival_location_list, departure_date_list, arrival_date_list=None):
        self._initialize_driver()
        
        if arrival_date_list is None:
            arrival_date_list = ['' for _ in range(len(departure_date_list))]
        elif len(arrival_date_list) != len(departure_date_list):
            raise ValueError("As listas de datas de chegada e partida devem ter o mesmo tamanho.")
        
        scrapping_results = []
        for departure_location, arrival_location, departure_date, arrival_date in zip(departure_location_list, arrival_location_list, departure_date_list, arrival_date_list):
            self._search(departure_location, arrival_location, departure_date, arrival_date)
            self.driver.implicitly_wait(10)
            scrapping_results.append(self._scrape_search_result())          

        self._quit_driver()
        
        return scrapping_results

    # Iniciando o chromedriver
    def _initialize_driver(self):
        if not self.driver:
            self.driver = webdriver.Chrome(executable_path=self.driver_path)

    # Encerrando o chromedriver
    def _quit_driver(self):
        if self.driver:
            self.driver.quit()
    
    # Abrindo a página do clickbus
    def _open_clickbus_site(self):
        self._initialize_driver()
        if self.driver.current_url != 'https://www.clickbus.com.br/':
            self.driver.get('https://www.clickbus.com.br/')
            self.driver.implicitly_wait(10)
    
    # Realizando a pesquisa dado na página inicial do ClickBus
    def _search(self, departure_location, arrival_location, departure_date, arrival_date):
        self._open_clickbus_site()
        
        # Encontrar elementos de entrada
        input_origin_element = self.driver.find_element(By.XPATH, '//*[@id="origin"]')
        input_arrival_element = self.driver.find_element(By.XPATH, '//*[@id="destination"]')
        input_departure_date_element = self.driver.find_element(By.XPATH, '//*[@id="departure-date"]')
        
        # Preencher informações de origem e destino
        self._select_location(input_origin_element, departure_location)
        self._select_location(input_arrival_element, arrival_location)

        # Preencher data de partida
        input_departure_date_element.send_keys(departure_date)
        
        # Se caso houver um arrival_date específicado
        if arrival_date:
            button_text = 'Ida e Volta' # Conferir porque é fácil de mudar esse texto
            xpath = f'//div[text()="{button_text}"]'
            self.driver.find_element(By.XPATH, xpath).click()
            input_arrival_date_element = self.driver.find_element(By.XPATH, '//*[@id="return-date"]')
            input_arrival_date_element.send_keys(arrival_date)

        
        # Clicar no botão de pesquisa
        search_button = self.driver.find_element(By.ID, 'search-box-button')
        search_button.click()
        
    # Scraping os resultados da pesquisa
    def _scrape_search_result(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        search_results = soup.find(attrs={"data-testid": "search-results"})
        containers = search_results.find_all(attrs={"data-testid": "search-item-container"})
        results = {
            'company_name': [],
            'promotion_price': [],
            'no_promotion_price': [],
            'departure_date': [],
            'departure_time': [],
            'return_time': [],
            'return_date': [],
            'arrival_location': [],
            'departure_location': []
        }
        for container in containers:
            # Obter o nome da empresa
            company_element = container.find(class_=self.company_regex)
            company_name = company_element.get('data-content')

            # Obter preços (tanto de promoção quanto sem promoção)
            price_element = container.find(class_=self.price_regex)
            promotion_element = price_element.find('span', {'data-testid': 'is-promotion'})
            no_promotion_element = price_element.find('span', {'data-testid': 'is-not-promotion'})

            if not promotion_element:
                promotion_price = None
            else:
                promotion_text = promotion_element.text
                promotion_price = self._get_number_from_price(promotion_text)
                
            no_promotion_text = no_promotion_element.get_text(strip=True)
            no_promotion_price = self._get_number_from_price(no_promotion_text)
            
            # Obter informações de data e hora de partida e retorno
            date_element = container.find(class_=self.hour_regex)
            departure_element = date_element.find("time", class_="departure-time")
            departure_date_string = departure_element.get('data-date')
            departure_date = datetime.strptime(departure_date_string, "%Y-%m-%d")
            departure_time = departure_element.get_text(strip=True)

            return_element = date_element.find("time", class_="return-time")
            return_element_list = return_element.get_text(strip=True).split('+')
            return_time = return_element_list[0]
            plus_days = int(return_element_list[1][0]) if len(return_element_list) > 1 else 0

            return_date_unformatted = departure_date + timedelta(days=plus_days)
            return_date = return_date_unformatted.strftime("%Y-%m-%d")

            # Obter informações de localização
            location_element = container.find(class_=re.compile(r"\w*bus-station"))
            departure_location_element = location_element.find(class_='station-departure')
            departure_location = departure_location_element.get_text(strip=True)
            arrival_location_element = location_element.find(class_='station-arrival')
            arrival_location = arrival_location_element.get_text(strip=True)
            
            # Adicionar resultados à estrutura de dados
            results['company_name'].append(company_name)
            results['no_promotion_price'].append(no_promotion_price)
            results['promotion_price'].append(promotion_price)
            results['departure_time'].append(departure_time)
            results['departure_date'].append(departure_date)
            results['return_time'].append(return_time)
            results['return_date'].append(return_date)
            results['arrival_location'].append(arrival_location)
            results['departure_location'].append(departure_location)
            
        return results

    def _select_location(self, input_element, location):
        input_element.send_keys(location)
        wait = WebDriverWait(self.driver, 3)
        wait.until(EC.presence_of_element_located((By.ID, 'place-input-ul')))
        sugestoes_div = self.driver.find_element(By.ID, 'place-input-ul')
        primeiro_a_element = sugestoes_div.find_element(By.TAG_NAME, 'a')
        primeiro_a_element.click()
        
    def _get_number_from_price(self, price_text):
        return float(price_text.replace('R$', '').replace('\xa0', '').replace(",", "."))



# Teste = ClickBusScraper()


# departure_location_list = ['Belo Horizonte', 'Belo Horizonte']
# arrival_location_list = ['São Paulo', 'Rio de Janeiro']
# departure_date_list = ['27/05/2023', '28/06/2023']
# result = Teste.scrape(departure_location_list, arrival_location_list, departure_date_list)

# Teste._initialize_driver()

# departure_location = 'Belo Horizonte'
# arrival_location = 'Rio de Janeiro'
# departure_date = '28/06/2023'
# arrival_date = ''
# Teste._search(departure_location, arrival_location, departure_date, arrival_date)
# Teste._scrape_search_result()
