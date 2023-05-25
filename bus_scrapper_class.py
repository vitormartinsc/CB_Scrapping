#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 25 11:16:09 2023

@author: vitor
"""


class Bus_scrapper:
    def __init__(
            self, link_bh_sp, departure_location_field, 
            arrival_location_field, departure_date_field, 
            search_table_class, 
            arrival_date_field = None
            ):
        self.link_bh_sp = link_bh_sp
        self.departure_location_field = departure_location_field
        self.arrival_location_field = arrival_location_field
        self.departure_date_field = departure_date_field
        self.arrival_date_field = arrival_date_field
        self.search_table_class = search_table_class
        