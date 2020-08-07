import asyncio
import requests
import os
import aiohttp
import datetime
import multiprocessing

from tornado.options import define, parse_command_line, options

from utils import get_req_url, get_names

define("ip", type=str, default="127.0.0.1")
define("port", type=int, default=8888)
define("api_name", type=str, default="/say/hello")
define("params", type=str, default="name=Lucy")
define("task_num", type=int, default=5)
define("process_num", type=int, default=3)

parse_command_line()


async def request(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    # result, status = await response.text()
    result, status = await response.text(), response.status
    await session.close()
    return result, status


def loop_request_wrapper(params):
    start = datetime.datetime.now()
    urls = [get_req_url(options, "name=".format(params[1])) for _ in range(options.task_num)]
    tasks = [asyncio.ensure_future(request(url)) for url in urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    end = datetime.datetime.now()
    print("visit %s" % (urls))
    print("my pid: %s, parent pid: %s, start at %s, end at %s" % (os.getpid(), os.getppid(), start, end))
    print('-' * 80)


if __name__ == "__main__":
    print(datetime.datetime.now())
    cpu_count = multiprocessing.cpu_count()
    print("cpu count:", cpu_count)
    pool = multiprocessing.Pool(cpu_count)

    names = get_names(options.process_num)
    params = [(i, names[i]) for i in range(options.process_num)]
    pool.map(loop_request_wrapper, params)
    pool.close()
    pool.join()
    print(datetime.datetime.now())
