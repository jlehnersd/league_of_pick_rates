#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 13:17:50 2019

@author: jeremy_lehner
"""

import pandas as pd
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os.path
from os import path

def get_champion_names(scrape=True, save=True):
    """
    Scrapes champion names from League of Legends Wiki,
      returns pandas series of names as strings

    Parameters
    ----------
    scrape : boolean
             Attempt to scrape champion names?
    save   : boolean
             Save list of names to csv file?

    Returns
    -------
    names : pandas series
            Contains champion names as strings
    """

    if scrape:
        url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions'
        names = pd.read_html(url)[1]

        names = list(names['Champion'])
        names = [s.split(',')[0] for s in names]
        names = [s.split('\xa0the')[0] for s in names]
        names = pd.Series(names).rename('champion')
        
        if save:
            names.to_csv('./data/champion_names.csv', index=False)

    elif path.exists('./data/champion_names.csv'):
        names = pd.read_csv('./data/champion_names.csv',
                            header=None,
                            squeeze=True)
    else:
        print('champion_names.csv file cannot be found!')
        names = []
    
    return names


def get_champion_release_dates(scrape=True, save=True):
    """
    Scrapes champion release dates from League of Legends Wiki,
      returns pandas series of dates as strings

    Parameters
    ----------
    scrape : boolean
             Attempt to scrape champion release dates?
    save   : boolean
             Save list of release dates to csv file?

    Returns
    -------
    dates : pandas series
            Contains champion release dates as strings 'YYYY-MM-DD'
    """

    if scrape:
        url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions'
        dates = pd.read_html(url)[1]

        dates = dates['Release Date'].rename('release_date')

        if save:
            dates.to_csv('./data/champion_release_dates.csv', index=False)

    elif path.exists('./data/champion_release_dates.csv'):
        dates = pd.read_csv('./data/champion_release_dates.csv',
                            header=None,
                            squeeze=True)
    else:
        print('champion_release_dates.csv file cannot be found!')
        dates = []
    
    return dates


def get_number_of_skins(names, scrape=True, save=True):
    """
    Scrapes number of champion skins from League of Legends Wiki,
      returns pandas series of number of skins as integers

    Parameters
    ----------
    names  : pandas series
             Contains all of the champion names as strings
    scrape : boolean
             Attempt to scrape number of skins for each champion?
    save   : boolean
             Save list of number of champion skins to csv file?

    Returns
    -------
    names : pandas series
            Contains number of champion skins as integers
    """

    if scrape:
        # Set up selenium web driver
        driver = webdriver.Chrome()

        # Get number of skins
        num_skins = []
        for name in names:
            name = name.replace(' ', '_')
            skins_url = f'https://leagueoflegends.fandom.com/wiki/{name}/Skins'
            driver.get(skins_url)
            time.sleep(1)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            num_skins.append(len(soup.find_all('div',
                {'style':'display:inline-block; margin:5px; width:342px'})))

        num_skins = pd.Series(num_skins)
        driver.close()

        if save:
            num_skins.to_csv('./data/num_skins.csv', index=False)

    elif path.exists('./data/num_skins.csv'):
        num_skins = pd.read_csv('./data/num_skins.csv',
                                header=None,
                                squeeze=True)
    else:
        print('num_skins.csv file cannot be found!')
        num_skins = []

    return num_skins