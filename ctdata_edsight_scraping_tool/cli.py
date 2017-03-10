# -*- coding: utf-8 -*-
import json
import sys

import click

from .links_prep import rebuild

# Import sync or async version of fetching routine
if sys.version_info[0:2] >= (3, 5):
    from .fetch_async import fetch_async as fetcher
else:
    from .fetch_sync import fetch_sync as fetcher


BASE_URL = 'http://edsight.ct.gov/SASPortal/main.do'
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/45.0.2454.101 Safari/537.36'),
}


with open("ctdata_edsight_scraping_tool/datasets.json", 'r') as f:
    links = json.load(f)


@click.group()
def main(args=None):
    """Console script for ctdata_edsight_scraping_tool"""

@main.command()
@click.option('--dataset', '-d',
              required=True,
              help="Name of the dataset to retrieve. Should conform to names output by the info cmd.")
@click.option('--output_dir',
              '-o',
              required=True,
              help="Full or relative path for storing downloaded files.",
              default='./')
@click.option('--variable',
              '-v',
              required=True,
              multiple=True,
              help="Variable to fetch. Can be multiple in which case each combination will be fetched")
def fetch(dataset, output_dir, variable):
    """Download the csv file of the dataset to a target directory.

    On Python versions below 3.5, fetching can take a few minutes or more to complete. This because each dataset is
    requested in sequence. In Python 3.5 and 3.6, the data requests happen asynchronously which results in significant
    performance gains.
    """
    fetcher(dataset, output_dir, variable)

@main.command()
@click.option('--target', required=True)
def refresh(target):
    """Update the dataset manifest file with a refreshed list of possible variables."""
    rebuild(target)

@main.command()
def datasets(args=None):
    """List datasets that are available for scraping"""
    for d in links.items():
        click.echo(d[0])

@main.command()
@click.option('--dataset', required=True,)
@click.option('--variable', required=False)
def info(dataset, variable):
    """Information about a dataset. Takes dataset name as an argument."""
    filters = links[dataset]['filters']
    if variable:
        var = [f for f in filters if f['name'] == variable][0]
        options = var['options']
        click.echo("\n`{}` has the following options available:\n".format(variable))
    else:
        options = [f['name'] for f in filters]
        click.echo("\n`{}` has the following variables available:\n".format(dataset))
    for o in options:
        click.echo("- {}".format(o))

if __name__ == "__main__":
    main()