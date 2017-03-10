#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_ctdata_edsight_scraping_tool
----------------------------------

Tests for `ctdata_edsight_scraping_tool` module.
"""

import pytest

from contextlib import contextmanager
from click.testing import CliRunner


@pytest.fixture
def dataset():
    return {
        "dataset": "Chronic Absenteeism",
        "link": "http://edsight.ct.gov/SASStoredProcess/do?_program=%2FCTDOE%2FEdSight%2FRelease%2FReporting%2FPublic%2FReports%2FStoredProcesses%2FChronicAbsenteeismReport&_select=Submit&_parampass=Yes",
        "download_link": "http://edsight.ct.gov/SASStoredProcess/do?_program=/CTDOE/EdSight/Release/Reporting/Public/Reports/StoredProcesses/ChronicAbsenteeismExport&_year=2015-16&_district=+&_subgroup=All+Students&_school=+",
        "filters": [
            {
                "name": "Year",
                "xpath_id": "_year",
                "options": ["Trend", "2015-16", "2014-15", "2013-14", "2012-13", "2011-12"]
            },
            {
                "name": "District",
                "xpath_id": "_district",
                "options": ["State of Connecticut", "All Districts"]
            },
            {
                "name": "School",
                "xpath_id": "_school",
                "options": ["All Schools"]
            }, {
                "name": "Filter By",
                "xpath_id": "_subgroup",
                "options": ["All Students", "Race/Ethnicity", "Gender", "Special Education Status",
                            "Free/Reduced Price Meal Eligibility", "English Learner Status", "Grade"]
            }]
    }

def test_single_var_params_list_generation(dataset):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    from ctdata_edsight_scraping_tool.fetch_async import build_params_list
    params = build_params_list(dataset, {}, ['Year'])
    assert params == [{'_year': 'Trend'}, {'_year': '2015-16'}, {'_year': '2014-15'}, {'_year': '2013-14'}, {'_year': '2012-13'}, {'_year': '2011-12'}]


def test_two_var_params_list_generation(dataset):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    from ctdata_edsight_scraping_tool.fetch_async import build_params_list
    params = build_params_list(dataset, {}, ['Year', 'Filter By'])
    assert params == [
        {'_year': 'Trend', '_subgroup': 'All Students'},
        {'_year': 'Trend', '_subgroup': 'Race/Ethnicity'},
        {'_year': 'Trend', '_subgroup': 'Gender'}, {'_year': 'Trend', '_subgroup': 'Special Education Status'},
        {'_year': 'Trend', '_subgroup': 'Free/Reduced Price Meal Eligibility'},
        {'_year': 'Trend', '_subgroup': 'English Learner Status'}, {'_year': 'Trend', '_subgroup': 'Grade'},
        {'_year': '2015-16', '_subgroup': 'All Students'}, {'_year': '2015-16', '_subgroup': 'Race/Ethnicity'},
        {'_year': '2015-16', '_subgroup': 'Gender'}, {'_year': '2015-16', '_subgroup': 'Special Education Status'},
        {'_year': '2015-16', '_subgroup': 'Free/Reduced Price Meal Eligibility'},
        {'_year': '2015-16', '_subgroup': 'English Learner Status'}, {'_year': '2015-16', '_subgroup': 'Grade'},
        {'_year': '2014-15', '_subgroup': 'All Students'}, {'_year': '2014-15', '_subgroup': 'Race/Ethnicity'},
        {'_year': '2014-15', '_subgroup': 'Gender'}, {'_year': '2014-15', '_subgroup': 'Special Education Status'},
        {'_year': '2014-15', '_subgroup': 'Free/Reduced Price Meal Eligibility'},
        {'_year': '2014-15', '_subgroup': 'English Learner Status'}, {'_year': '2014-15', '_subgroup': 'Grade'},
        {'_year': '2013-14', '_subgroup': 'All Students'}, {'_year': '2013-14', '_subgroup': 'Race/Ethnicity'},
        {'_year': '2013-14', '_subgroup': 'Gender'}, {'_year': '2013-14', '_subgroup': 'Special Education Status'},
        {'_year': '2013-14', '_subgroup': 'Free/Reduced Price Meal Eligibility'},
        {'_year': '2013-14', '_subgroup': 'English Learner Status'}, {'_year': '2013-14', '_subgroup': 'Grade'},
        {'_year': '2012-13', '_subgroup': 'All Students'}, {'_year': '2012-13', '_subgroup': 'Race/Ethnicity'},
        {'_year': '2012-13', '_subgroup': 'Gender'}, {'_year': '2012-13', '_subgroup': 'Special Education Status'},
        {'_year': '2012-13', '_subgroup': 'Free/Reduced Price Meal Eligibility'},
        {'_year': '2012-13', '_subgroup': 'English Learner Status'}, {'_year': '2012-13', '_subgroup': 'Grade'},
        {'_year': '2011-12', '_subgroup': 'All Students'}, {'_year': '2011-12', '_subgroup': 'Race/Ethnicity'},
        {'_year': '2011-12', '_subgroup': 'Gender'}, {'_year': '2011-12', '_subgroup': 'Special Education Status'},
        {'_year': '2011-12', '_subgroup': 'Free/Reduced Price Meal Eligibility'},
        {'_year': '2011-12', '_subgroup': 'English Learner Status'}, {'_year': '2011-12', '_subgroup': 'Grade'}]


def test_get_xpaths(dataset):
    from ctdata_edsight_scraping_tool.fetch_async import get_xpaths
    xpaths = get_xpaths(dataset['filters'], ['Year', 'Filter By'])
    assert xpaths == ['_year', '_subgroup']

def test_url_list_builder():
    from ctdata_edsight_scraping_tool.fetch_async import build_url_list

    xpaths = ['_year', '_subgroup']

    params = [
        {'_year': 'Trend', '_subgroup': 'All Students'},
        {'_year': 'Trend', '_subgroup': 'Race/Ethnicity'},
        {'_year': '2011-12', '_subgroup': 'All Students'},
        {'_year': '2011-12', '_subgroup': 'Race/Ethnicity'}
    ]

    targets = [{'url': 'http://test.com', 'param': {'_year': 'Trend', '_subgroup': 'All Students'},
      'filename': './test_Trend_All-Students.csv'},
     {'url': 'http://test.com', 'param': {'_year': 'Trend', '_subgroup': 'Race/Ethnicity'},
      'filename': './test_Trend_Race-Ethnicity.csv'},
     {'url': 'http://test.com', 'param': {'_year': '2011-12', '_subgroup': 'All Students'},
      'filename': './test_2011-12_All-Students.csv'},
     {'url': 'http://test.com', 'param': {'_year': '2011-12', '_subgroup': 'Race/Ethnicity'},
      'filename': './test_2011-12_Race-Ethnicity.csv'}]

    outputs = build_url_list(params, xpaths, 'http://test.com', './', 'test')

    assert outputs == targets
