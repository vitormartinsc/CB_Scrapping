# ClickBus Scraper

Este é um projeto de web scraping usando Selenium e BeautifulSoup para extrair informações de resultados de pesquisa no site ClickBus.

## Requisitos

- Python 3.7 ou superior
- ChromeDriver (certifique-se de ter o ChromeDriver instalado e configurado)
- pandas (instalado automaticamente a partir do requirements.txt)
- selenium
- beautifulsoup4

Você pode instalar os pacotes necessários executando o seguinte comando:
```shell
pip install -r requirements.txt
```

## Instalação

Clone o repositório:
```bash
git clone https://github.com/seu-usuario/clickbus-scraper.git
```

## Configuração

Certifique-se de ter o driver do Selenium adequado para o seu navegador instalado. Atualmente, o projeto está configurado para usar o driver do Google Chrome. 

Coloque o arquivo busscraper_input.xlsx na mesma pasta do arquivo main.py. Certifique-se de que o arquivo Excel tenha a seguinte estrutura:

| departure_location | arrival_location | departure_date | arrival_date |
| ------------------ | ---------------- | -------------- | ------------ |
| São Paulo          | Rio de Janeiro   | 2023-05-25     |              |
| Rio de Janeiro    | São Paulo        | 2023-05-26     |              |
| .... | ... | ...  |              |

Preencha as informações das localizações de partida, localizações de chegada e datas de partida. As datas de chegada são opcionais e podem ser deixadas em branco.

## Executando o Scraper

Para executar o scraper, abra o terminal e navegue até o diretório do projeto. Em seguida, execute o seguinte comando:
```shell
python main.py
```
O programa irá iniciar o processo de scraping das informações de passagens de ônibus no site ClickBus. Os resultados serão salvos em um arquivo CSV chamado clickbus_results.csv.

## Arquivo CSV de Resultados

O arquivo CSV de resultados conterá as seguintes informações para cada itinerário:

- Nome da empresa de ônibus
- Preço promocional (se disponível)
- Preço sem promoção
- Horário de partida
- Horário de retorno
- Data de retorno (se aplicável)
- Localização de chegada
- Localização de partida

Certifique-se de verificar o arquivo CSV gerado após a execução do programa para acessar os resultados obtidos.



