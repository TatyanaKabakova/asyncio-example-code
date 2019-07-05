import asyncio
import aiohttp

import requests
from time import time

"""
url = 'https://loremflickr.com/320/240/'


def get_file(get_url):
    r = requests.get(get_url, allow_redirects=True)
    return r


def write_file(response):
    # https://loremflickr.com/cache/resized/2720_4097907932_eb208f3042_n_320_240_nofilter.jpg
    filename = response.url.split('/')[-1]
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    t0 = time()

    file_url = 'https://loremflickr.com/320/240/'

    for i in range(10):
        write_file(get_file(file_url))

    print(time() - t0)


if __name__ == '__main__':
    main()
"""

# # # # # # # # # # # # # # # # # #


def write_image(data):
    filename = 'file-{}.jpeg'.format(int(time() * 1000))
    with open(filename, 'wb') as file:
        file.write(data)


async def fetch_content(get_url, i):
    t2 = time()
    async with aiohttp.ClientSession() as session:
        async with session.get(get_url, allow_redirects=True) as response:
            print('fetch_content', i, time()-t2)
            data = await response.read()
            write_image(data)


async def main2():
    # file_url = 'https://loremflickr.com/320/240/'
    file_url = 'https://loremflickr.com/cache/resized/2720_4097907932_eb208f3042_n_320_240_nofilter.jpg'
    tasks = []

    # one session for all requests in original
    # async with aiohttp.ClientSession() as session:
    #     for i in range(10): ...
    for i in range(10):
        # task = asyncio.create_task(fetch_content(file_url, session, i))
        task = fetch_content(file_url, i)
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    t0 = time()
    asyncio.run(main2())
    print(time() - t0)


# !! session per request because of https://github.com/aio-libs/aiohttp/issues/3698
