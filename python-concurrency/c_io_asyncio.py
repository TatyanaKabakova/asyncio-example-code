import asyncio
import time
import aiohttp


async def download_site(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print("Read {0} from {1}".format(response.content_length, url))


async def download_all_sites(sites):
    # one session for all requests in original
    # async with aiohttp.ClientSession() as session:
    #     tasks = [] ...
    tasks = []
    for url in sites:
        task = asyncio.ensure_future(download_site(url))
        tasks.append(task)
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 80
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(download_all_sites(sites))
    duration = time.time() - start_time
    print(f"Downloaded {len(sites)} sites in {duration} seconds")


# !! session per request because of https://github.com/aio-libs/aiohttp/issues/3698
