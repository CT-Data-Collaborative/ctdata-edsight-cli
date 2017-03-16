#     CT SDE EdSight Data Scraping Command Line Interface.
#     Copyright (C) 2017  Sasha Cuerda, Connecticut Data Collaborative
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import urllib
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
                target_url_query = urllib.parse.urlencode(t['param'])

                click.echo("\n\nDownloading: {}\n{}\nfrom {}{}".format(dataset,
                                                                     os.path.basename(t['filename']),
                                                                     t['url'],target_url_query))
                response = s.get(t['url'], params=t['param'])
                if save:
                    with open(t['filename'], 'wb') as file:
                        file.write(response.content)
