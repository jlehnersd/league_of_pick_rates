#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 13:17:50 2019

@author: jeremy_lehner
"""

import pandas as pd
import os.path
from os import path

def get_champion_names(scrape=True, save=True):
    """
    Scrapes champion names from League of Legends Wiki, returns list of names

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
            names.to_csv('./data/names.csv', index=False)

    elif path.exists('./data/names.csv'):
        names = pd.read_csv('./data/names.csv', header=None)
    else:
        print('names.csv file cannot be found!')
        names = []
    return names