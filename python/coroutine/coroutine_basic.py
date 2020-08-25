#!/usr/bin/env python3

import asyncio
import time

from concurrent.futures import ThreadPoolExecutor


def work(t: int):
	print("now:", time.time(), "will sleee {} seconds".format(t))
	time.sleep(t)
	return t + 1


async def main(loop, t: int):
	executor = ThreadPoolExecutor()
	return await loop.run_in_executor(executor, work, t)

start = time.time()
loop = asyncio.get_event_loop()
co1 = main(loop, 1)
co2 = main(loop, 2)
tasks = [
	asyncio.ensure_future(co1),
	asyncio.ensure_future(co2)
]
dones, _ = loop.run_until_complete(asyncio.wait(tasks))
print("total time: ", time.time() - start)  # 大约2秒

for r in dones:
	print('Task ret: ', r.result())

for task in tasks:
	print('Task ret: ', task.result())

loop.close()
