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


def fetch_sync(dataset, output_dir, geography, catalog, save=True):
    """Download the csv file of the dataset to a target directory."""
    targets = _setup_download_targets(dataset, output_dir, geography, catalog)
    with requests.session() as s:
        s.get(BASE_URL)

        click.echo("Fetching {}\n\n".format(dataset))
        with progressbar.ProgressBar(max_value=len(targets)) as bar:
            for i, t in enumerate(targets):
                bar.update(i)
                target_url_query = urllib.parse.urlencode(t['param']).replace('%2F', '/')

                # click.echo("\n\nDownloading: {}\nFrom: {}?{}".format(os.path.basename(t['filename']),
                #                                                         t['url'],target_url_query))

                ATTEMPTS = 0
                STATUS_CODE = 0
                data = '<html>'
                while ATTEMPTS < 4 and STATUS_CODE != 200 and data.find('<html>') != -1:
                    try:
                        response = s.get(t['url'], params=t['param'])
                    except Exception as e:
                        click.echo(e)
                        STATUS_CODE = 0
                        continue
                    STATUS_CODE = response.status_code
                    data = response.text
                    target_url = response.url
                if save and STATUS_CODE == 200:
                    # Lets check to make sure that the content is an actual CSV files with results
                    no_results = data.find('The query you have run did not contain any results.') != -1
                    bad_response = data.find('<html>') != -1
                    if not no_results and not bad_response:
                        with open(t['filename'], 'wb') as file:
                            file.write(response.content)
                    elif no_results:
                        click.echo("\n{} failed.\nThe query you have run did not contain any results.\n".format(target_url))
                    elif bad_response:
                        click.echo("\n{} failed.\bBad response from the EdSight server.\n".format(target_url))
                    else:
                        click.echo("\n{} failed.\bSomething unexpected happened.".format(target_url))
                else:
                    click.echo("We had an issue with this dataset. Please try again.")
