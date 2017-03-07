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
    do_not_keep = ['', ' ', '  ', '   ']
    target = browser.find_element_by_xpath('//*[@name="{}"]'.format(name))
    choices = target.find_elements_by_tag_name('option')
    return [c.text for c in choices if c.text not in do_not_keep]

def build_variable_object(browser, name, xpath_id):
    if xpath_id == '_school':
        browser.find_element_by_xpath('//option[contains(text(), "All Districts")]').click()
    options = get_options(browser, xpath_id)
    return {'name': name, 'xpath_id': xpath_id, 'options': options}

def scrape_dataset(browser, dataset):
    browser.get(dataset['link'])
    vars = dataset['filters']
    new_var_object = [build_variable_object(browser, k, v) for k,v in vars.items()]
    return { 'dataset': dataset['dataset'], 'link': dataset['link'], 'filters': new_var_object }

def build_links_object_json():
    browser = setup_chrome_browser()
    browser.get('http://edsight.ct.gov')
    with open("ctdata_edsight_scraping_tool/links.json", 'r') as f:
        links = json.load(f)
    return {k:scrape_dataset(browser, v) for k,v in links.items() }

def rebuild(outfile):
    new_links = build_links_object_json()
    with open(outfile, 'w') as f:
        json.dump(new_links, f)
