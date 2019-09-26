#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 20:38:06 2019

@author: jeremy_lehner
"""

import pandas as pd
import glob


def get_patches_since_change(last_patch):
    """
    Determines the number of patches since each champion was changed as of
      patch 9.18

    Parameters
    ----------
    last_patch : pandas series
                 Contains the last patch each champion was changed as strings

    Returns
    -------
    patches_since_change : pandas series
                           Contains number of patches since last change as ints
    """

    # Construct list of patches from current patch to oldest
    patches = '9.18 9.17 9.16 9.15 9.14 9.13 9.12 9.11 9.10 9.9 9.8 9.7 9.6 \
               9.5 9.4 9.3 9.2 9.1 8.24b 8.24 8.23 8.22 8.21 8.20 8.19 8.18 \
               8.17 8.16 8.15 8.14 8.13 8.12 8.11 8.10 8.9 8.8 8.7 8.6 8.5 \
               8.4 8.3 8.2 8.1 7.24b 7.24 7.23 7.22'.split()

    # Set number of patches since last change starting with 1 for 9.18 change
    patches_since_change = pd.Series(patches.index(s)+1 for s in last_patch)

    return patches_since_change


def combine_rate_data(win, ban, pick):
    """
    Creates one data frame of dynamic data over patch 9.18 from individual
      win rate, ban rate, and pick rate data frames

    Parameters
    ----------
    win  : pandas data frame
           Contains win rates for each champ on each day of data
    ban  : pandas data frame
           Contains ban rates for each champ on each day of data
    pick : pandas data frame
           Contains pick rates for each champ on each day of data

    Returns
    -------
    dynamic_df : pandas data frame
                 Contains the combined daily win, ban, and pick rates as floats
    """

    # Extract individual series to use in combined data frame
    date = win['date']
    winrates = win['winrate']
    banrates = ban['banrate']
    pickrates = pick['pickrate']

    # Combine into single data frame
    dynamic_df = pd.concat([date, winrates, banrates, pickrates], axis=1)

    return dynamic_df


def repeat_each_day(static_df, num_days):
    """
    Stacks rows of the data frame containing static league data over patch 9.18
      according to the number of days for which data was collected

    Parameters
    ----------
    static_df : pandas data frame
                Contains all data that did not change over the course of 9.18
    num_day   : integer
                Number of days for which data was collected during patch 9.18

    Returns
    -------
    repeat_df : pandas data frame
                Data frame where rows of static_df are stacked num_days times
    """

    # Create list of num_days copies of static_df
    static_copies = []
    for copy_number in range(0, num_days):
        static_copies.append(static_df)

    # Combine copies into one data frame
    repeat_df = pd.concat(static_copies, ignore_index=True)

    return repeat_df


def get_champ_age(release_dates, data_dates):
    """
    Calculates the age of each champion in days on each data that data was
      collected during patch 9.18

    Parameters
    ----------
    release_date : pandas series
                   Release dates for each champion as strings 'YYYY-MM-DD'
    data_date    : pandas series
                   Dates on which data was collected as strings 'YYYY-MM-DD'

    Returns
    -------
    champ_age : pandas series
                Contains the age of each champion on each day as integers
    """

    # Convert dates to datetime objects
    release_dates = pd.to_datetime(release_dates)
    data_dates = pd.to_datetime(data_dates)

    # Calculate champions ages
    champ_age = (data_dates - release_dates).dt.days

    return champ_age
