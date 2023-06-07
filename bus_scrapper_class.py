import re
import pdb
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains



class ClickBusScraper:
    # Atualizar o driver_path de acordo com o caminho local para o chromedriver
    def __init__(self, driver_path='/usr/local/bin/chromedriver'):
        self.driver_path = driver_path
        self.driver = None
        # Experessões regulares que serão úteis para encontrar elementos html mais tarde
        self.company_regex = re.compile(r"\w*company")
        self.price_regex = re.compile(r"\w*price")
        self.hour_regex = re.compile(r"\w*hour")
        
    def scrape(self, departure_location_list, arrival_location_list, departure_date_list, return_date_list=None):
        self._initialize_driver()
        
        if len(departure_location_list) != len(arrival_location_list):
            raise ValueError("As listas de locais de chegada e partida devem ter o mesmo tamanho.")
        
        if return_date_list is None:
            return_date_list = [float('nan') for _ in range(len(departure_date_list))]
        elif len(return_date_list) != len(departure_date_list):
            raise ValueError("As listas de datas de chegada e partida devem ter o mesmo tamanho.")
        
        scrapping_results = []
        search_id = 1
        for departure_location, arrival_location, departure_date, return_date in zip(departure_location_list, arrival_location_list, departure_date_list, return_date_list):
            self._search(departure_location, arrival_location, departure_date, return_date)
            self.driver.implicitly_wait(10)
            scrape_results = self._scrape_search_result(return_date)
            if not scrape_results:
                continue
            for scrape_result in scrape_results:
                scrape_result_len = len(scrape_result['company_name'])
                scrape_result['search_id'] = [search_id for _ in range(scrape_result_len)]
            scrapping_results += scrape_results
            search_id += 1
                
        self._quit_driver()
        
        return scrapping_results

    # Iniciando o chromedriver
    def _initialize_driver(self):
        if not self.driver:
            self.driver = webdriver.Chrome(executable_path=self.driver_path)
            return
        
        if not self._is_driver_alive():
            self.driver = webdriver.Chrome(executable_path=self.driver_path)
            return

    def _is_driver_alive(self):
        try:
           self.driver.current_url
           return True
        except:
           return False 
            
    
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
    def _search(self, departure_location, arrival_location, departure_date, return_date):
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
        
        # Se caso houver um return_date específicado
        # valores nulos não são iguais a eles mesmos no python
        if return_date == return_date:
            button_text = 'Ida e Volta' # Conferir porque é fácil de mudar esse texto
            xpath = f'//div[text()="{button_text}"]'
            self.driver.find_element(By.XPATH, xpath).click()
            input_return_date_element = self.driver.find_element(By.XPATH, '//*[@id="return-date"]')
            input_return_date_element.send_keys(return_date)

        
        # Clicar no botão de pesquisa
        search_button = self.driver.find_element(By.ID, 'search-box-button')
        search_button.click()
        
    # Scraping os resultados da pesquisa
    def _scrape_search_result(self, return_date=float('nan')):
        has_return_date = return_date == return_date
        
        
        results = {
            'company_name': [],
            'promotion_price': [],
            'no_promotion_price': [],
            'departure_date': [],
            'departure_time': [],
            'arrival_time': [],
            'arrival_date': [],
            'arrival_location': [],
            'departure_location': [],
            'class': []
        }
        div_classe = self.driver.find_element(By.XPATH, '//div[h3[contains(text(), "Classe")]]')
        spans = div_classe.find_elements(By.CSS_SELECTOR, 'span[class*="search-filter-item"]')
        #pdb.set_trace()
        for span in spans:
            class_text = span.text
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-testid="checkbox-wrapper"]')))
            checkbox_wrapper = span.find_element(By.CSS_SELECTOR, 'div[data-testid="checkbox-wrapper"]')
            #ActionChains(self.driver).move_to_element(checkbox_wrapper).click(checkbox_wrapper).perform()            
            try:
                checkbox_wrapper.click()
            except ElementClickInterceptedException:
                pass
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            search_results = soup.find(attrs={"data-testid": "search-results"})
            # Não há resultado na pesquisa
            if search_results == None:
                continue
            containers = search_results.find_all(attrs={"data-testid": "search-item-container"})
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
    
                arrival_element = date_element.find("time", class_="return-time")
                arrival_element_list = arrival_element.get_text(strip=True).split('+')
                arrival_time = arrival_element_list[0]
                plus_days = int(arrival_element_list[1][0]) if len(arrival_element_list) > 1 else 0
    
                arrival_date_unformatted = departure_date + timedelta(days=plus_days)
                arrival_date = arrival_date_unformatted.strftime("%Y-%m-%d")
    
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
                results['arrival_time'].append(arrival_time)
                results['arrival_date'].append(arrival_date)
                results['arrival_location'].append(arrival_location)
                results['departure_location'].append(departure_location)
                results['class'].append(class_text)    
        
            time.sleep(3)
            while True:
                try:
                    checkbox_wrapper.click()
                    break
                except ElementClickInterceptedException:
                    time.sleep(1)
                

            
        results_len = len(results['company_name'])
        
        # Não apareceu nenhum resultado
        if not results_len:
            return False

        if has_return_date:
            while True:
                try:
                    self._change_to_return_options()
                except (NoSuchElementException, ElementClickInterceptedException):
                    self.driver.refresh()
                    continue
                else:
                    break
            results_departure = results
            results_departure['has_return'] = [True for _ in range(results_len)]
            results_departure['type'] = ['Departure' for _ in range(results_len)]
            results_return = self._scrape_search_result()[0]
            results_return_len = len(results_return['company_name'])
            results_return['has_return'] = [True for _ in range(results_return_len)]
            results_return['type'] = ['Return' for _ in range(results_return_len)]
            results = [results_return, results_departure]
            return results

        else:   
            results['has_return'] = [False for _ in range(results_len)]
            results['type'] = ['Departure' for _ in range(results_len)]
            return [results]
    
    def _change_to_return_options(self):
        select_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Selecionar')]")
        select_button.click()
        #wait = WebDriverWait(self.driver, 10)
        seat_items = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="seatmap-item"]')
        for seat_item in seat_items:
           seat_number_label = seat_item.find_element(By.CSS_SELECTOR, '.seat-number-label')
           if seat_number_label.text:
               try:
                   seat_item.click()
                   break
               except ElementClickInterceptedException:
                   print("Clique interceptado. Tentando outro elemento...")
                   continue
        self._click_continue_booking()
        self._wait_for_page_load()
        return True
    
    def _wait_for_page_load(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.staleness_of(self.driver.find_element(By.XPATH, '//div[contains(text(), "Reservando seu assento")]')))
            print("Página totalmente carregada. Continue a raspagem.")
        except TimeoutException:
            print("Tempo limite de espera excedido. A página pode não ter sido totalmente carregada.")

    def _click_continue_booking(self):
        continue_button = self.driver.find_element(By.CSS_SELECTOR, '.continue-booking')
        self.driver.execute_script("arguments[0].click();", continue_button)
        
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

# # Teste._initialize_driver()
# Teste = ClickBusScraper()

# departure_location = 'Belo Horizonte'
# arrival_location = 'Rio de Janeiro'
# departure_date = '28/06/2023'
# return_date = '03/07/2023'
# Teste._search(departure_location, arrival_location, departure_date, return_date)
# results = Teste._scrape_search_result(return_date)

# bt = a.find_element(By.XPATH, "//button[contains(text(), 'Selecionar')]")
# bt.click()
# wait = WebDriverWait(a, 10)
# bt2 = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Continuar a reserva')]")))
# bt2.click()
# wait = WebDriverWait(a, 10)
# seat_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="seatmap-item"]')))
# seat_element.click()

