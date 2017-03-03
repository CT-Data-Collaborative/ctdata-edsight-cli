# -*- coding: utf-8 -*-
import json
import click

with open("ctdata_edsight_scraping_tool/links.json", 'r') as f:
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
@click.argument('dataset', required=True,)
def info(dataset):
    """Information about a dataset. Takes dataset name as an argument."""
    filters = links[dataset]['filters']
    filter_names = [k for k,v in filters.items()]
    click.echo("\n`{}` has the following variables available:\n".format(dataset))
    for f in filter_names:
        click.echo("- {}".format(f))

if __name__ == "__main__":
    main()
