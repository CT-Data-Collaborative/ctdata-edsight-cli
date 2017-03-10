import json
import asyncio
import aiofiles
import aiohttp
from urllib.parse import urlparse, parse_qs
from itertools import product

from pkg_resources import resource_string
links = json.loads(resource_string(__name__, 'dataset.json'))

BASE_URL = 'http://edsight.ct.gov/SASPortal/main.do'
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/45.0.2454.101 Safari/537.36'),
}


def build_params_list(dataset, base_qs, variables):
    filters = list(product(*[f['options'] for f in dataset['filters'] if f['name'] in variables]))
    param_options = [f['xpath_id'] for f in dataset['filters'] if f['name'] in variables]
    params = []
    for i, f in enumerate(filters):
        new_qs = {**base_qs}
        for idx, p in enumerate(param_options):
            new_qs[p] = f[idx]
        for k,v in new_qs.items():
            if not isinstance(v, str):
                new_qs[k] = v[0]
        params.append(new_qs)
    return params


def setup_download_targets(dataset, output_dir, variable):
    """Download the csv file of the dataset to a target directory."""
    ds = links[dataset]
    ds_filters = ds['filters']
    xpaths = [f['xpath_id'] for f in ds_filters if f['name'] in variable]
    dl_link = ds['download_link']
    dl_parsed = urlparse(dl_link)
    qs = parse_qs(dl_parsed.query)
    new_url = dl_parsed._replace(query=None).geturl()
    params = build_params_list(ds, qs, variable)
    targets = []
    for p in params:
        f = [p[v] for v in xpaths]
        filename_variables = '_'.join(f)
        slug = filename_variables.replace('/', '-').replace(' ', '-')
        filename = "{}{}_{}.csv".format(output_dir, dataset, slug)
        targets.append({'url': new_url, 'param': p, 'filename': filename})
    return targets


async def get_report(url, params, file):
    print('Getting {}\n'.format(file))
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as context:
            pass
        async with session.get(url, headers=HEADERS, params=params) as resp:
            data = await resp.text()
        async with aiofiles.open(file, 'w') as f:
            await f.write(data)



def fetch_async(dataset, output_dir, variables):
    targets = setup_download_targets(dataset, output_dir, variables)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            *(get_report(t['url'], t['param'], t['filename']) for t in targets)
        )
    )

