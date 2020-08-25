#!/usr/bin/env python3

import asyncio
import time
import random

from concurrent.futures import ThreadPoolExecutor

# 控制最大并发为200
semaphore = asyncio.Semaphore(200)


def work(t: int):
	print("now:", time.time(), "will sleee {} seconds".format(t))
	time.sleep(t)
	return t + 1


async def main(loop, t: int):
	async with semaphore:
		executor = ThreadPoolExecutor()
		return await loop.run_in_executor(executor, work, t)


start = time.time()
loop = asyncio.get_event_loop()
tasks = []
for i in range(1000):
	tasks.append(main(loop, random.randint(2, 2)))

dones, _ = loop.run_until_complete(asyncio.wait(tasks))
print("total time: ", time.time() - start)

for r in dones:
	# print('Task ret: ', r.result())
	pass
#
# for task in tasks:
# 	print('Task ret: ', task.result())

loop.close()
