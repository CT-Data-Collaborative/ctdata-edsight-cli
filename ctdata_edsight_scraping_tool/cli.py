# -*- coding: utf-8 -*-
import json
from urllib.parse import urlparse, parse_qs

import click
import requests
import progressbar

from itertools import product

from .links_prep import rebuild

with open("ctdata_edsight_scraping_tool/datasets.json", 'r') as f:
    links = json.load(f)

@click.group()
def main(args=None):
    """Console script for ctdata_edsight_scraping_tool"""


@main.command()
@click.option('--dataset', '-d', help="Name of the dataset to retrieve. Should conform to names output by the info "
                                      "cmd.")
@click.option('--output_dir', '-o', help="Full or relative path for storing downloaded files.", default='./')
@click.option('--variable', '-v', required=True, multiple=True, help="Variable to loop over when requesting data. Can be "
                                                           "multiple in whcih case each combination will be fetched")
def fetch(dataset, output_dir, variable):
    """Download the csv file of the dataset to a target directory."""
    ds = links[dataset]
    dl_link = ds['download_link']
    dl_parsed = urlparse(dl_link)
    qs = parse_qs(dl_parsed.query)
    new_url = dl_parsed._replace(query=None).geturl()
    filters = list(product(*[f['options'] for f in ds['filters'] if f['name'] in variable]))
    parem_options = [f['xpath_id'] for f in ds['filters'] if f['name'] in variable]
    with requests.session() as s:
        s.get('http://edsight.ct.gov/SASPortal/main.do')
        new_qs = {**qs}
        with progressbar.ProgressBar(max_value=len(filters)) as bar:
            for i, f in enumerate(filters):
                bar.update(i)
                click.echo("\n\nFetching:    {} {}".format(dataset, " - ".join(f)))
                for idx, p in enumerate(parem_options):
                    new_qs[p] = f[idx]
                    filename_variables = '_'.join(f)
                    slug = filename_variables.replace('/', '-')
                    filename = "{}/{}_{}.csv".format(output_dir, dataset, slug)
                    with open(filename, 'wb') as file:
                        response = s.get(new_url, params=new_qs)
                        file.write(response.content)

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
