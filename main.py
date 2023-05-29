#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 26 12:50:15 2023

@author: vitor
"""

import pandas as pd
from bus_scrapper_class import ClickBusScraper


def main():
    # departure_location_list = ['São Paulo', 'Rio de Janeiro', 'Belo Horizonte']
    # arrival_location_list = ['Curitiba', 'Florianópolis', 'Porto Alegre']
    # departure_date_list = ['23/06/2023', '01/06/2023', '03/06/2023']
    # arrival_date_list = ['01/07/2023', '', '']
    df_scraper_input =  pd.read_excel('busscraper_input.xlsx')
    departure_location_list = df_scraper_input.departure_location
    arrival_location_list = df_scraper_input.arrival_location
    departure_date_list = df_scraper_input.departure_date.dt.strftime("%d/%m/%Y")
    arrival_date_list = df_scraper_input.arrival_date.dt.strftime("%d/%m/%Y")

    scraper = ClickBusScraper()
    results = scraper.scrape(
        departure_location_list,
        arrival_location_list,
        departure_date_list,
        arrival_date_list
    )

    merged_dataframes = merge_dataframes(results)
    merged_dataframes.to_csv('clickbus_results.csv')

def merge_dataframes(results):
    dfs = []
    for result in results:
        new_df = pd.DataFrame(result)
        dfs.append(new_df)
    return pd.concat(dfs)


if __name__ == '__main__':
    main()  