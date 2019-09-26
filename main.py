#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 13:49:27 2019

@author: jeremy_lehner
"""

# Import required modules and functions
import os.path
from os import path
import sys
import requests
import time
import random
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary

# Import custom functions for this project
from src.get_league_data import get_champion_names
from src.get_league_data import get_champion_release_dates
from src.get_league_data import get_number_of_skins
from src.get_league_data import get_win_rates
from src.get_league_data import get_ban_rates
from src.get_league_data import get_pick_rates
from src.get_league_data import get_last_patch_change
from src.get_league_data import get_scrape_date

from src.scrape_league_data import scrape_champ_names
from src.scrape_league_data import scrape_release_dates
from src.scrape_league_data import scrape_number_of_skins
from src.scrape_league_data import scrape_win_rates
from src.scrape_league_data import scrape_ban_rates
from src.scrape_league_data import scrape_pick_rates
from src.scrape_league_data import scrape_last_patch_change
from src.scrape_league_data import get_scrape_date

#date_data = get_scrape_date()
#
champ_names = get_champion_names()
#
#champ_release_dates = get_champion_release_dates()
#
#num_skins = get_number_of_skins(champ_names)
#
#win_rates = get_win_rates(date_data, scrape=True, save=True)
#
#ban_rates = get_ban_rates(date_data, scrape=True, save=True)
#
#pick_rates = get_pick_rates(date_data, scrape=True, save=True)
#
#last_patch = get_last_patch_change(champ_names)

# Scrape data if you don't want to use the data already available
scrape = False
if scrape:
    scrape_champ_names()
    scrape_release_dates()
    scrape_number_of_skins(champ_names)
    scrape_win_rates()
    scrape_ban_rates()
    scrape_pick_rates()
    scrape_last_patch_change(champ_names)

# Load the data