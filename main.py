#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 13:49:27 2019

@author: jeremy_lehner
"""

# import necessary functions
import os.path
from os import path
import pandas as pd

from src.get_league_data import get_champion_names
from src.get_league_data import get_champion_release_dates


champ_names = get_champion_names()

champ_release_dates = get_champion_release_dates()
