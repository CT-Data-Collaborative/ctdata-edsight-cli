import click
import requests
import progressbar

from .helpers import _setup_download_targets

BASE_URL = 'http://edsight.ct.gov/SASPortal/main.do'

def fetch_sync(dataset, output_dir, variable, catalog, save=True):
    """Download the csv file of the dataset to a target directory."""
    targets = _setup_download_targets(dataset, output_dir, variable, catalog)
    with requests.session() as s:
        s.get(BASE_URL)

        with progressbar.ProgressBar(max_value=len(targets)) as bar:
            for i, t in enumerate(targets):
                bar.update(i)
                click.echo("\n\nFetching: {} {} at {}".format(dataset, t['filename'], t['url']))
                response = s.get(t['url'], params=t['param'])
                if save:
                    with open(t['filename'], 'wb') as file:
                        file.write(response.content)
