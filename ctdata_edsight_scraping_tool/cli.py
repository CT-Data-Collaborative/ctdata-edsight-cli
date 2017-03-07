# -*- coding: utf-8 -*-
import json
import click
import requests
from bs4 import BeautifulSoup

with open("ctdata_edsight_scraping_tool/datasets.json", 'r') as f:
    links = json.load(f)

@click.group()
def main(args=None):
    """Console script for ctdata_edsight_scraping_tool"""


@main.command()
def list(args=None):
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
