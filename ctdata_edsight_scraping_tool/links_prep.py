# -*- coding: utf-8 -*-
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
    do_not_keep = ['', ' ', '  ', '   ']
    target = browser.find_element_by_xpath('//*[@name="{}"]'.format(name))
    choices = target.find_elements_by_tag_name('option')
    return [c.text for c in choices if c.text not in do_not_keep]

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

def build_links_object_json():
    """Launch a chrome browser and kick off the scraping"""
    browser = setup_chrome_browser()
    browser.get('http://edsight.ct.gov')
    with open("datasets.json", 'r') as f:
        links = json.load(f)
    links_object = {k:scrape_dataset(browser, v) for k,v in links.items() }
    browser.quit()
    return links_object

def rebuild(outfile):
    """Take a file path name, rebuild the dataset manifest and write to the new file"""
    new_links = build_links_object_json()
    with open(outfile, 'w') as f:
        json.dump(new_links, f)
