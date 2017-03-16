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
import os
import urllib
import click
import requests
import progressbar

from .helpers import _setup_download_targets

BASE_URL = 'http://edsight.ct.gov/SASPortal/main.do'

def fetch_sync(dataset, output_dir, variable, catalog, save=True, mute=False):
    """Download the csv file of the dataset to a target directory."""
    targets = _setup_download_targets(dataset, output_dir, variable, catalog)
    with requests.session() as s:
        s.get(BASE_URL)

        click.echo("Fetching {}\n\n".format(dataset))
        with progressbar.ProgressBar(max_value=len(targets)) as bar:
            for i, t in enumerate(targets):
                bar.update(i)
                target_url_query = urllib.parse.urlencode(t['param']).replace('%2F', '/')

                if not mute:
                    click.echo("\n\nDownloading: {}\nFrom: {}?{}".format(os.path.basename(t['filename']),
                                                                        t['url'],target_url_query))

                ATTEMPTS = 0
                STATUS_CODE = 0
                while ATTEMPTS < 3 and STATUS_CODE != 200:
                    try:
                        response = s.get(t['url'], params=t['param'])
                    except Exception as e:
                        click.echo(e)
                        STATUS_CODE = 0
                        continue
                    STATUS_CODE = response.status_code
                if save and STATUS_CODE == 200:
                    with open(t['filename'], 'wb') as file:
                        file.write(response.content)
                else:
                    click.echo("We had an issue with this dataset. Please try again.")
