# -*- coding: utf-8 -*-
import os
import time
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


BASE_URL = 'http://edsight.ct.gov/SASPortal/main.do'

CWD = os.getcwd()
DL_DIR = os.path.join(CWD, "scraping", "capacity", "data_scraping")

DATASET_LINKS = {'Attendance': '', 'Discipline': '', 'English Language Learners': '',
                 'Enrollment': '', 'Students with Disabilities': '', 'Demographics': '',
                 'Qualifications': '', 'Staffing Levels': '', 'CMT': '', 'Postsecondary': '',
                 'Graduation Rates': '', 'K3': '', 'Fitness': '', 'SAT': '', 'Smarter Balenced': '',
                 }


def district_to_dict(district):
    id, name = district.split("-")
    return {'id': int(id), 'district': name}

def get_year_element(year_str):
    xpath = "//select[@id='pickyr']/option[text()='{}']".format(year_str)
    return browser.find_element_by_xpath(xpath)

def get_district_element(district_str):
    """Take a string representing a district choice text and return the element for further work"""
    xpath = "//*[@id='picktown']/option[@value={}]".format(district_str)
    return browser.find_element_by_xpath(xpath)


def select_district(district_str, *args):
    """Take a district string, get the element and select it"""
    d = get_district_element(district_str)
    d.click()
    for a in args:
        a()


def select_year(year):
    y = get_year_element(year)
    y.click()

def select_category():
    xpath = '//*[@id="aspnetForm"]/div[6]/table/tbody/tr[11]/td[1]/input'
    bullet = browser.find_element_by_xpath(xpath)
    bullet.click()

def get_select_options(xpath):
    options = browser.find_elements_by_xpath(xpath)
    return [d.text for d in options]

def get_year_strings():
    return get_select_options("//select[@id='pickyr']/option")

def get_district_strings(skip_first=False):
    """Get all the options and extract the text"""
    district_strings = get_select_options("//select[@name='picktown']/option")
    if skip_first:
        return [d for d in district_strings[1:]]
    else:
        return district_strings


def click_button(xpath):
    try:
        button = browser.find_element_by_xpath(xpath)
    except NoSuchElementException as e:
        raise e
    button.click()

def click_download_csv_button():
    dl_button = browser.find_element_by_xpath("//a[@title='click here to download this data as a comma separated file']")
    dl_button.click()

def rename_download(basename, district_str, name_suffix=None):
    """Files get a generic name when downloaded. Rename as district"""
    dname = district_str.split("-")[1]
    slug = dname.lower().replace(" ", "-").replace('.', '').replace('/', '-')
    if name_suffix:
        new_name = "{}_{}.csv".format(slug, name_suffix)
    else:
        new_name = "{}.csv".format(slug)
    target = os.path.join(DL_DIR, new_name)
    for filename in os.listdir(DL_DIR):
        if filename.startswith(basename):
            source = os.path.join(DL_DIR, filename)
            os.rename(source, target)


def setup_chrome_browser():
    """Pass in configs to chrome browser"""
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"download.default_directory": DL_DIR}
    chromeOptions.add_experimental_option("prefs", prefs)
    chromedriver = '/usr/local/bin/chromedriver'
    os.environ["webdriver.chrome.driver"] = chromedriver
    browser = webdriver.Chrome(chromedriver, chrome_options=chromeOptions)
    return browser



def write_district_xwalk(districts):
    """Helper function for saving the district crosswalk"""
    district_dict = [district_to_dict(d) for d in districts]
    with open('district_xwalk.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'district'])
        writer.writeheader()
        for row in district_dict:
            writer.writerow(row)


def select_summary_button():
    browser.find_element_by_xpath("//input[@value='2']").click()


failed = []
def scrape(browser, districts, years):
    for d in districts:
        for y in years:
            browser.get(BASE_URL)
            print("Fetching: {}, {}".format(d, y))
            try:
                d_id = d.split("-")[0]
                select_district(d_id)
            except:
                failed.append((d,y))
                continue
            select_year(y)
            select_category()
            time.sleep(1)
            # fetch results
            try:
                click_button('//*[@id="buttonA"]/a[1]')
                time.sleep(1)
            except NoSuchElementException:
                failed.append((d,y))
                browser.get(BASE_URL)
                continue
            # download
            try:
                click_button("//a[@title='click here to download this data as a comma separated file']")
                time.sleep(1)
            except NoSuchElementException:
                failed.append((d, y))
                browser.get(BASE_URL)
                continue
            try:
                rename_download(basename="ed050_pub", district_str=d, name_suffix=y)
            except FileNotFoundError:
                time.sleep(2)
                rename_download(basename="ed050_pub", district_str=d, name_suffix=y)
            time.sleep(1)

def combine():
    """Combine all of the downloaded CSVs into one list. Also use crosswalks to add some fields for easier reading"""


    # Load the district crosswalk
    with open('scraping/capacity/district_xwalk.csv', 'r') as file:
        reader = csv.DictReader(file)
        lookup = {row['id']: row['district'] for row in reader}

    fnames = ['Year', 'Town', 'district', 'district_id', 'sch_type', 'sch_name', 'sch_co', 'erg', 'sq_feet', 'acre',
              'port_n', 'port_yr', 'capacity', 'class_rm', 'enroll']

    with open('school_capacity_2_15_17.csv', 'w') as file:
        writer = csv.DictWriter(file, fnames)
        writer.writeheader()

    for filename in os.listdir(DL_DIR):
        if filename == '.DS_Store':
            pass
        else:
            # year = re.search('(\d+)', filename).group()
            p = os.path.join(DL_DIR, filename)
            with open(p, 'r') as file:
                reader = csv.DictReader(file)
                print(filename)
                for row in reader:
                    try:
                        row['district'] = lookup[row['Town']]
                    except KeyError:
                        row['district'] = ''
                    row['district_id'] = row['Town']
                    row['sch_name'] = row['sch_name'].rstrip()
                    row['Year'] = '2013'
                    del row['']
                    with open('school_capacity_2_15_17.csv', 'a') as file:
                        writer = csv.DictWriter(file, fnames)
                        writer.writerow(row)


def run(districts):
    try:
        browser = setup_chrome_browser()
        browser.get(BASE_URL)
        years = get_year_strings()
        scrape(browser, districts, years)
    except:
        pass
    # finally:
    # # combine()
    #     browser.close()
    #     browser.quit()

if __name__ == '__main__':
    run()


dl_files = [filenames for filenames in os.listdir(DL_DIR)]
unique_dls = []
for f in dl_files:
    district = f.split('_')[0]
    if district in unique_dls:
        pass
    else:
        unique_dls.append(district)

districts_to_dl = [d.split('-')[1] for d in districts]

missing_districts = []
for d in districts_to_dl:
    fd = d.lower().replace(" ", "-")
    if fd not in unique_dls:
        missing_districts.append(d)

districts_to_redl = []
for d in districts:
    if d.split('-')[1] in missing_districts:
        districts_to_redl.append(d.rstrip())

scrape(browser, districts_to_redl, years)
combine()


districts = get_district_strings()
scrape(browser, districts, ['2013'])
