#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 09:06:22 2019

@author: jeremy_lehner
"""

import pandas as pd
from os import path
import glob


def load_champ_names():
    """
    Loads the champion names from a csv file,
      returns them as a pandas series

    Parameters
    ----------
    None

    Returns
    -------
    names : pandas series
            Contains champion names as strings
    """

    if path.exists('./data/champion_names.csv'):
        names = pd.read_csv('./data/champion_names.csv',
                            header=None,
                            squeeze=True)
    else:
        print('champion_names.csv cannot be found (._.)')
        names = []

    return names


def load_release_dates():
    """
    Loads the champion release dates from a csv file,
      returns them as a pandas series

    Parameters
    ----------
    None

    Returns
    -------
    dates : pandas series
            Contains champion release dates as strings 'YYYY-MM-DD'
    """

    if path.exists('./data/champion_release_dates.csv'):
        dates = pd.read_csv('./data/champion_release_dates.csv',
                            header=None,
                            squeeze=True)
    else:
        print('champion_release_dates.csv file cannot be found (._.)')
        dates = []

    return dates


def load_number_of_skins():
    """
    Loads the number of skins for each champion from a csv file,
      returns them as a pandas series

    Parameters
    ----------
    None

    Returns
    -------
    num_skins : pandas series
                Contains number of champion skins as integers
    """

    if path.exists('./data/num_skins.csv'):
        num_skins = pd.read_csv('./data/num_skins.csv',
                                header=None,
                                squeeze=True)
    else:
        print('num_skins.csv file cannot be found (._.)')
        num_skins = []

    return num_skins


def load_win_rates():
    """
    Loads the champion win rates and correspdonding dates from csv files,
      returns them in a pandas data frame

    Parameters
    ----------
    None

    Returns
    -------
    winrates_all : pandas data frame
                   Contains champion win rates as floats and dates as strings
    """

    path = './data/win/'
    files = glob.glob(path + '*.csv')

    winrates = []
    for file in files:
        winrates.append(pd.read_csv(file))

    winrates_all = pd.concat(winrates, ignore_index=True)

    return winrates_all


def load_ban_rates():
    """
    Loads the champion ban rates and correspdonding dates from csv files,
      returns them in a pandas data frame

    Parameters
    ----------
    None

    Returns
    -------
    banrates_all : pandas data frame
                   Contains champion ban rates as floats and dates as strings
    """

    path = './data/ban/'
    files = glob.glob(path + '*.csv')

    banrates = []
    for file in files:
        banrates.append(pd.read_csv(file))

    banrates_all = pd.concat(banrates, ignore_index=True)

    return banrates_all


def load_pick_rates():
    """
    Loads the champion pick rates and correspdonding dates from csv files,
      returns them in a pandas data frame

    Parameters
    ----------
    None

    Returns
    -------
    pickrates_all : pandas data frame
                    Contains champion pick rates as floats and dates as strings
    """

    path = './data/pick/'
    files = glob.glob(path + '*.csv')

    pickrates = []
    for file in files:
        pickrates.append(pd.read_csv(file))

    pickrates_all = pd.concat(pickrates, ignore_index=True)

    return pickrates_all


def load_last_patch_change():
    """
    Loads the last patch each champion was changed from csv files
      returns them as a pandas data frame

    Parameters
    ----------
    None

    Returns
    -------
    last_patch : pandas series
                 Contains last patch each champion was changed as strings
    """

    if path.exists('./data/last_patch.csv'):
        last_patch = pd.read_csv('./data/last_patch.csv',
                                 header=None,
                                 squeeze=True)
        last_patch = last_patch.astype('str')
        
    else:
        print('last_patch.csv file cannot be found (._.)')
        last_patch = []

    return last_patch
