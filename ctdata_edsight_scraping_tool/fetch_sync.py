from urllib.parse import urlparse, parse_qs
from itertools import product

import click
import requests
import progressbar


with open("datasets.json", 'r') as f:
    links = json.load(f)


def fetch_sync(dataset, output_dir, variable):
    """Download the csv file of the dataset to a target directory."""
    ds = links[dataset]
    dl_link = ds['download_link']
    dl_parsed = urlparse(dl_link)
    qs = parse_qs(dl_parsed.query)
    new_url = dl_parsed._replace(query=None).geturl()
    filters = list(product(*[f['options'] for f in ds['filters'] if f['name'] in variable]))
    parem_options = [f['xpath_id'] for f in ds['filters'] if f['name'] in variable]
    with requests.session() as s:
        s.get(BASE_URL)
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
