#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 16:43:33 2019

@author: jeremy_lehner
"""

import pandas as pd
import datetime
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from os import path


def get_scrape_date():
    """
    Gets the date on which data was scraped

    Parameters
    ----------
    None

    Returns
    -------
    date : string
           Date that data was scraped in the format 'YYYY-MM-DD'
    """

    # Get current date and time
    now = datetime.datetime.now()
    year_scraped = str(now.year)
    month_scraped = str(now.month)
    day_scraped = str(now.day)

    # Add leading zeroes to single-digit months and days
    if len(month_scraped) == 1:
        month_scraped = '0' + month_scraped
    if len(day_scraped) == 1:
        day_scraped = '0' + day_scraped

    # Construct date string
    date_data = year_scraped + '-' + month_scraped + '-' + day_scraped

    # Bye! <3
    return date_data


def scrape_champ_names(save=True):
    """
    Scrapes champion names from League of Legends Wiki and saves them to
      csv file, but returns nothing

    Parameters
    ----------
    save   : boolean
             Save names to csv file?

    Returns
    -------
    None
    """

    # Assign scrape path variables
    url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions'

    # Get champion names
    names = pd.read_html(url)[1]

    names = list(names['Champion'])
    names = [s.split(',')[0] for s in names]
    names = [s.split('\xa0the')[0] for s in names]
    names = pd.Series(names).rename('champion')

    # Write names to csv file
    if save:
        names.to_csv('./data/champion_names.csv', index=False)

    # Bye! <3
    return


def scrape_release_dates(save=True):
    """
    Scrapes champion release dates from League of Legends Wiki and saves them
      to csv file, but returns nothing

    Parameters
    ----------
    save   : boolean
             Save release dates to csv file ('YYYY-MM-DD')?

    Returns
    -------
    None
    """

    # Assign scrape path variables
    url = 'https://leagueoflegends.fandom.com/wiki/List_of_champions'

    # Get release dates
    dates = pd.read_html(url)[1]
    dates = dates['Release Date'].rename('release_date')

    # Write release dates to csv file
    if save:
        dates.to_csv('./data/champion_release_dates.csv', index=False)

    # Bye! <3
    return


def scrape_number_of_skins(names, save=True):
    """
    Scrapes number of champion skins from League of Legends Wiki and saves
      them to a csv file, but returns nothing

    Parameters
    ----------
    names  : pandas series
             Contains the champion names as strings in alphabetical order
    save   : boolean
             Save number of champion skins to csv file?

    Returns
    -------
    None
    """

    # Assign scrape path variables
    style = 'display:inline-block; margin:5px; width:342px'

    # Set up selenium web driver
    driver = webdriver.Chrome('./src/utils/chromedriver')

    # Get number of skins
    num_skins = []
    for name in names:
        name = name.replace(' ', '_')
        skins_url = f'https://leagueoflegends.fandom.com/wiki/{name}/Skins'
        driver.get(skins_url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        num_skins.append(len(soup.find_all('div', {'style': style})))

    num_skins = pd.Series(num_skins)

    # Close selenium web driver
    driver.close()

    if save:
        num_skins.to_csv('./data/num_skins.csv', index=False)

    # Bye! <3
    return


def scrape_win_rates(save=True):
    """
    Scrapes the current day North America champion win rates from op.gg and
      saves them to a csv file along with the date, but returns nothing

    Parameters
    ----------
    save : boolean
           Save win rates as csv file?

    Returns
    -------
    None
    """

    # Get date at time of scraping
    date = get_scrape_date()

    # Assign scraping variables
    champstats_url = 'https://na.op.gg/statistics/champion/'
    today_xpath = '//*[@id="recent_today"]/span/span'
    winrate_xpath = '//*[@id="rate_win"]/span/span'
    scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
    champs = 'Champion.1'
    win = 'Win rate'

    # Set up selenium web driver
    driver = webdriver.Chrome('./src/utils/chromedriver')
    driver.get(champstats_url)

    # Select stats for current day
    today_button = driver.find_element_by_xpath(today_xpath)
    today_button.click()

    # Select win rates
    winrate_button = driver.find_element_by_xpath(winrate_xpath)
    winrate_button.click()

    # Scroll to bottom of page and wait to bypass ads
    driver.execute_script(scroll_down)
    time.sleep(10)

    # Scrape win rates
    winrates = pd.read_html(driver.page_source)[1]
    winrates = winrates[[champs, win]]

    # Sort win rates by champion in alphabetical order
    winrates.sort_values(by=champs, inplace=True)
    winrates = winrates[win].reset_index()[win]

    # Close selenium web driver
    driver.close()

    # Convert win rates to float
    winrates = winrates.str.replace('%', '')
    winrates = round(winrates.astype('float')/100, 4)

    # Add a column with the date
    winrates = pd.DataFrame({'winrate': winrates, 'date': date})

    # Write win rates to csv file
    if save:
        date = date.replace('-', '')
        winrates.to_csv(f'./data/win/win_rates_{date}.csv', index=False)
    else:
        print('Win rates were scraped, but not saved!')

    # Bye! <3
    return


def scrape_ban_rates(save=True):
    """
    Scrapes the current day North America champion ban rates from op.gg and
      saves them to a csv file along with the date, but returns nothing

    Parameters
    ----------
    save   : boolean
             Save ban rates as csv file?

    Returns
    -------
    None
    """

    # Get date at time of scraping
    date = get_scrape_date()

    # Assign scraping variables
    champstats_url = 'https://na.op.gg/statistics/champion/'
    today_xpath = '//*[@id="recent_today"]/span/span'
    banrate_xpath = '//*[@id="rate_ban"]/span/span'
    scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
    champs = 'Champion.1'
    ban = 'Ban ratio per game'

    # Set up selenium web driver
    driver = webdriver.Chrome('./src/utils/chromedriver')
    driver.get(champstats_url)

    # Select stats for current day
    today_button = driver.find_element_by_xpath(today_xpath)
    today_button.click()

    # Select ban rates
    banrate_button = driver.find_element_by_xpath(banrate_xpath)
    banrate_button.click()

    # Scroll to bottom of page and wait to bypass ads
    driver.execute_script(scroll_down)
    time.sleep(10)

    # Scrape ban rates
    banrates = pd.read_html(driver.page_source)[1]
    banrates = banrates[[champs, ban]]

    # Sort ban rates by champion in alphabetical order
    banrates.sort_values(by=champs, inplace=True)
    banrates = banrates[ban].reset_index()[ban]

    # Close Selenioum web driver
    driver.close()

    # Convert ban rates to float
    banrates = banrates.str.replace('%', '')
    banrates = round(banrates.astype('float')/100, 4)

    # Add a column with the date
    banrates = pd.DataFrame({'banrate': banrates, 'date': date})

    # Write ban rates to csv file
    if save:
        date = date.replace('-', '')
        banrates.to_csv(f'./data/ban/ban_rates_{date}.csv', index=False)
    else:
        print('Ban rates were scraped, but not saved!')

    # Bye! <3
    return banrates


def scrape_pick_rates(save=True):
    """
    Scrapes the current day North America champion pick rates from op.gg and
      saves them to a csv file along with the date, but returns nothing

    Parameters
    ----------
    save   : boolean
             Save pick rates as csv file?

    Returns
    -------
    None
    """

    # Get date at time of scraping
    date = get_scrape_date()

    # Assign scraping variables
    champstats_url = 'https://na.op.gg/statistics/champion/'
    today_xpath = '//*[@id="recent_today"]/span/span'
    pickrate_xpath = '//*[@id="rate_pick"]/span/span'
    scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
    champs = 'Champion.1'
    pick = 'Pick ratio per game'

    # Set up selenium web driver
    driver = webdriver.Chrome('./src/utils/chromedriver')
    driver.get(champstats_url)

    # Select stats for current day
    today_button = driver.find_element_by_xpath(today_xpath)
    today_button.click()

    # Select pick rates
    pickrate_button = driver.find_element_by_xpath(pickrate_xpath)
    pickrate_button.click()

    # Scroll to bottom of page and wait to bypass ads
    driver.execute_script(scroll_down)
    time.sleep(10)

    # Scrape pick rates
    pickrates = pd.read_html(driver.page_source)[1]
    pickrates = pickrates[[champs, pick]]

    # Sort ban rates by champion in alphabetical order
    pickrates.sort_values(by=champs, inplace=True)
    pickrates = pickrates[pick].reset_index()[pick]

    # Close selenium web driver
    driver.close()

    # Convert pick rates to float
    pickrates = pickrates.str.replace('%', '')
    pickrates = round(pickrates.astype('float')/100, 4)

    # Add a column with the date
    pickrates = pd.DataFrame({'pickrate': pickrates, 'date': date})

    # Write pick rates to csv file
    if save:
        date = date.replace('-', '')
        pickrates.to_csv(f'./data/pick/pick_rates_{date}.csv', index=False)
    else:
        print('Pick rates were scraped, but not saved!')

    # Bye! <3
    return pickrates


def scrape_last_patch_change(names, save=True):
    """
    Scrapes the last patch in which each champion was changed from League Wiki
      and saves them to a csv file, but returns nothing

    Parameters
    ----------
    names  : pandas series
             Contains the champion names as strings in alphabetical order
    save   : boolean
             Save the last patch each champion was changed to csv file?

    Returns
    -------
    None
    """

    # Set up selenium web driver
    driver = webdriver.Chrome('./src/utils/chromedriver')

    # Get patch when champion was last changed
    last_patch = []
    for name in names:
        name = name.replace(' ', '_')
        champ_url = f'https://lol.gamepedia.com/{name}#Patch_History'
        driver.get(champ_url)
        time.sleep(2)

        # Parse the champion page HTML
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Get entire patch history but only grab patch versions from HTML
        history = [link for link in soup.find_all('a')
                   if '>v1.' in str(link) or 'Patch 1.' in str(link)
                   or '>v2.' in str(link) or 'Patch 2.' in str(link)
                   or '>v3.' in str(link) or 'Patch 3.' in str(link)
                   or '>v4.' in str(link) or 'Patch 4.' in str(link)
                   or '>v5.' in str(link) or 'Patch 5.' in str(link)
                   or '>v6.' in str(link) or 'Patch 6.' in str(link)
                   or '>v7.' in str(link) or 'Patch 7.' in str(link)
                   or '>v8.' in str(link) or 'Patch 8.' in str(link)
                   or '>v9.' in str(link) or 'Patch 9.' in str(link)]

        # Get only the most recent patch in which the champion was changed
        most_recent = history[0]
        most_recent = str(most_recent)[-8:-4]
        last_patch.append(most_recent)

    # Close selenium web driver
    driver.close()

    # Standardize the patch version format
    for idx, patch in enumerate(last_patch):
        last_patch[idx] = patch.replace('v', '')
    for idx, patch in enumerate(last_patch):
        last_patch[idx] = patch.replace(' ', '')

    # Convert the patches into a pandas series
    last_patch = pd.Series(last_patch)

    # Write the patches to a csv file
    if save:
        last_patch.to_csv('./data/last_patch.csv', index=False)
    else:
        print('Patches were scraped, but not saved!')

    # Bye! <3
    return last_patch
