import asyncio
import itertools as it
import os
import random
import time


"""
a group of blocking producers serially add items to the queue, one producer at a time. 
Only after all producers are done can the queue be processed, by one consumer at a time processing item-by-item. 

The first few coroutines are helper functions that return a random string, a fractional-second performance counter, 
and a random integer. A producer puts anywhere from 1 to 5 items into the queue. Each item is a tuple of (i, t) 
where i is a random string and t is the time at which the producer attempts to put the tuple into the queue.

When a consumer pulls an item out, it simply calculates the elapsed time that the item sat in the queue using the 
timestamp that the item was put in with.

"""


async def makeitem(size: int = 5) -> str:
    return os.urandom(size).hex()


async def randsleep(a: int = 1, b: int = 5, caller=None) -> None:
    i = random.randint(0, 10)
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
    await asyncio.sleep(i)


async def produce(name: int, q: asyncio.Queue) -> None:
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):  # Synchronous loop for each single producer
        await randsleep(caller=f"Producer {name}")
        i = await makeitem()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Producer {name} added <{i}> to queue.")


async def consume(name: int, q: asyncio.Queue) -> None:
    while True:
        await randsleep(caller=f"Consumer {name}")
        i, t = await q.get()
        now = time.perf_counter()
        print(f"Consumer {name} got element <{i}>"
              f" in {now-t:0.5f} seconds.")
        q.task_done()


async def main(nprod: int, ncon: int):
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(nprod)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(ncon)]
    await asyncio.gather(*producers)
    await q.join()  # Implicitly awaits consumers, too
    for c in consumers:
        c.cancel()


if __name__ == "__main__":
    import argparse
    random.seed(444)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--nprod", type=int, default=5)
    parser.add_argument("-c", "--ncon", type=int, default=10)
    ns = parser.parse_args()
    start = time.perf_counter()
    asyncio.run(main(**ns.__dict__))
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.5f} seconds.")


"""
The challenging part of this workflow is that there needs to be a signal to the consumers that production is done. 
Otherwise, await q.get() will hang indefinitely, because the queue will have been fully processed, but consumers won’t 
have any idea that production is complete.

The key is to await q.join(), which blocks until all items in the queue have been received and processed, and then to 
cancel the consumer tasks, which would otherwise hang up and wait endlessly for additional queue items to appear.

"""
