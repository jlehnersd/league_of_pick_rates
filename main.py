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
#from src.get_league_data import get_champion_names
#from src.get_league_data import get_champion_release_dates
#from src.get_league_data import get_number_of_skins
#from src.get_league_data import get_win_rates
#from src.get_league_data import get_ban_rates
#from src.get_league_data import get_pick_rates
#from src.get_league_data import get_last_patch_change
#from src.get_league_data import get_scrape_date

# Import data scraping functions
from src.scrape_league_data import get_scrape_date
from src.scrape_league_data import scrape_champ_names
from src.scrape_league_data import scrape_release_dates
from src.scrape_league_data import scrape_number_of_skins
from src.scrape_league_data import scrape_win_rates
from src.scrape_league_data import scrape_ban_rates
from src.scrape_league_data import scrape_pick_rates
from src.scrape_league_data import scrape_last_patch_change

# Import data loading functions
from src.load_league_data import load_champ_names
from src.load_league_data import load_release_dates
from src.load_league_data import load_number_of_skins
from src.load_league_data import load_win_rates
from src.load_league_data import load_ban_rates
from src.load_league_data import load_pick_rates
from src.load_league_data import load_last_patch_change

# Import data processing functions
from src.process_league_data import get_patches_since_change
from src.process_league_data import repeat_each_day
from src.process_league_data import combine_rate_data
from src.process_league_data import get_champ_age


# Get the champion names and number of champions
champ_names = load_champ_names()
num_champs = len(champ_names)

# Scrape data if you don't want to use the data already available
champ_names = load_champ_names()
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
champ_names = load_champ_names()
release_dates = load_release_dates()
num_skins = load_number_of_skins()
win_rates = load_win_rates()
ban_rates = load_ban_rates()
pick_rates = load_pick_rates()
last_patch = load_last_patch_change()

# Get number of days
num_days = int(win_rates.shape[0]/num_champs)

# Combine dynamic win, ban, and pick rates into one data frame
dynamic = combine_rate_data(win_rates, ban_rates, pick_rates)

# Determine number of patches since champion was last changed
patches_since_change = get_patches_since_change(last_patch)

# Construct data frame for static features over patch 9.18
static_features = [champ_names, release_dates, num_skins, patches_since_change]
static = pd.concat(static_features, axis=1)
static.columns = ['champion',
                  'release_date',
                  'num_skins',
                  'patches_since_change']

# Repeat static data for each day data was scraped during patch 9.18
static = repeat_each_day(static, num_days)

# Combine static data with dynamic data
league_df = pd.concat([static, dynamic], axis=1)

# Determine the champion age on each day that data was collected
champ_age = get_champ_age(league_df['release_date'], league_df['date'])
league_df['champion_age'] = champ_age

# Select only the columns used for modeling (target = pickrate)
model_data = ['champion_age',
              'patches_since_change',
              'num_skins',
              'winrate',
              'banrate',
              'pickrate']
tidy_data = league_df[model_data]
