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


champ_names = get_champion_names(scrape=False, save=False)

champ_release_dates = get_champion_release_dates(scrape=False, save=False)

num_skins = get_number_of_skins(champ_names, scrape=False, save=False)

win_rates = get_win_rates(scrape=False, save=False)
