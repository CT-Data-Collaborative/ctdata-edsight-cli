import asyncio
import aiofiles
import aiohttp

from .helpers import _setup_download_targets

BASE_URL = 'http://edsight.ct.gov/SASPortal/main.do'
HEADERS = {
    'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/45.0.2454.101 Safari/537.36'),
}

# TODO Should move the sesssion context manager one level up so I can
# resuse across requests and so that I can add limitation to connection pool
async def get_report(url, params, file, save):
    print('Getting {} at {}\n'.format(file, url))

    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL, headers=HEADERS) as context:
            pass
        async with session.get(url, headers=HEADERS, params=params) as resp:
            data = await resp.text()
        if save:
            async with aiofiles.open(file, 'w') as f:
                await f.write(data)



def fetch_async(dataset, output_dir, variables, catalog, save=True):
    targets = _setup_download_targets(dataset, output_dir, variables, catalog)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            *(get_report(t['url'], t['param'], t['filename'], save) for t in targets)
        )
    )
