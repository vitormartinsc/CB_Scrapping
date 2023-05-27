# ClickBus Scraper

Este é um projeto de web scraping usando Selenium e BeautifulSoup para extrair informações de resultados de pesquisa no site ClickBus.

## Requisitos

- Python 3.7 ou superior
- ChromeDriver (certifique-se de ter o ChromeDriver instalado e configurado)
- pandas (instalado automaticamente a partir do requirements.txt)

## Instalação

1. Clone o repositório:
git clone https://github.com/seu-usuario/clickbus-scraper.git

2. Navegue até o diretório do projeto:
cd clickbus-scraper

3. Instale as dependências usando o pip:
pip install -r requirements.txt


## Como usar

1. Importe a classe `ClickBusScraper`:

```python
from clickbus_scraper import ClickBusScraper
```
2. Crie uma instância do ClickBusScraper:

```python
scraper = ClickBusScraper()

