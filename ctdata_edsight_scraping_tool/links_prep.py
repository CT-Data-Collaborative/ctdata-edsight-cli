# -*- coding: utf-8 -*-
#     CT SDE EdSight Data Scraping Command Line Interface.
#     Copyright (C) 2017  Sasha Cuerda, Connecticut Data Collaborative
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import json
import os
from selenium import webdriver


def setup_chrome_browser():
    """Pass in configs to chrome browser"""
    chromeOptions = webdriver.ChromeOptions()
    # prefs = {"download.default_directory": DL_DIR}
    # chromeOptions.add_experimental_option("prefs", prefs)
    chromedriver = '/usr/local/bin/chromedriver'
    os.environ["webdriver.chrome.driver"] = chromedriver
    browser = webdriver.Chrome(chromedriver, chrome_options=chromeOptions)
    return browser

def get_options(browser, name):
    """Does the actual work of getting the options and dropping empties"""
    do_not_keep = ['', '  ', '   ']
    target = browser.find_element_by_xpath('//*[@name="{}"]'.format(name))
    choices = target.find_elements_by_tag_name('option')
    results = []
    for c in choices:
        r = c.get_attribute('value')
        if r not in do_not_keep and r is not None:
            results.append(r)
        else:
            r = c.text
            if r not in do_not_keep and r is not None:
                results.append(r)
            else:
                pass
    return results

def build_variable_object(browser, variable):
    """For a given variable, get all of the options. Looking at schools requires that All Districts be selected"""
    name = variable['name']
    xpath_id = variable['xpath_id']
    if xpath_id == '_school':
        browser.find_element_by_xpath('//option[contains(text(), "All Districts")]').click()
    options = get_options(browser, xpath_id)
    return {'name': name, 'xpath_id': xpath_id, 'options': options}

def get_download_link(browser):
    """After a page has been loaded, locate and return the download link."""
    dl = browser.find_element_by_xpath(('//a[contains(text(), "Export .csv file")]'))
    return dl.get_attribute('href')


def scrape_dataset(browser, dataset):
    """Load a dataset link and get all the available filter options. Return a dict."""
    print(dataset['dataset'])
    browser.get(dataset['link'])
    download_link = get_download_link(browser)
    vars = dataset['filters']
    new_var_object = [build_variable_object(browser, v) for v in vars]
    return {
        'dataset': dataset['dataset'],
        'link': dataset['link'],
        'download_link': download_link,
        'filters': new_var_object
    }

def build_links_object_json(links):
    """Launch a chrome browser and kick off the scraping"""
    browser = setup_chrome_browser()
    browser.get('http://edsight.ct.gov')
    links_object = {k:scrape_dataset(browser, v) for k,v in links.items() }
    browser.quit()
    return links_object

def rebuild(links, outfile):
    """Take a file path name, rebuild the dataset manifest and write to the new file"""
    new_links = build_links_object_json(links)
    with open(outfile, 'w') as f:
        json.dump(new_links, f)

