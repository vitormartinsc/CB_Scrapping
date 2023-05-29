# ClickBus Scraper

Este é um projeto de web scraping usando Selenium e BeautifulSoup para extrair informações de resultados de pesquisa no site ClickBus.

## Requisitos

- Python 3.7 ou superior
- ChromeDriver (certifique-se de ter o ChromeDriver instalado e configurado)
- pandas (instalado automaticamente a partir do requirements.txt)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/clickbus-scraper.git
```

2. Navegue até o diretório do projeto:
```bash
cd clickbus-scraper
```

3. Instale as dependências usando o pip:
```bash
pip install -r requirements.txt
```

## Como usar

1. No arquivo main.py, defina as listas `departure_location_list`, `arrival_location_list`, `departure_date_list` e `arrival_date_list` com as informações desejadas.

2. Execute o arquivo main.py para iniciar o processo de scraping
```shell
python main.py
```

3. Após a conclusão do scraping, um arquivo CSV chamado clickbus_results.csv será gerado no diretório do projeto, contendo os resultados da pesquisa.
