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
define("task_num", type=int, default=10)
define("process_num", type=int, default=3)

parse_command_line()

cpu_count = multiprocessing.cpu_count()


async def request(url, params=None):
    print("my pid: %s, url: %s" % (os.getpid(), url))
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            if resp.status != 200:
                print('access {} failed: {}, retry ...', [resp.url, params], resp)
            else:
                result = await resp.text()
                # print("type of result: %s type resp.text(): %s" % (type(result), resp.text()))
                return result


def get_my_params(params, pid):
    pid = (pid % 10) % cpu_count
    every = len(params) // cpu_count
    if pid == cpu_count - 1:
        return params[pid * every:]
    return params[pid * every:(pid + 1) * every]


def loop_request_wrapper(params):
    # print("params:{}".format(params))
    my_params = get_my_params(params, os.getpid())
    start = datetime.datetime.now()
    urls = [get_req_url(options, ("name=%s" % (my_params[i][1],))) for i in range(len(my_params))]
    tasks = [asyncio.ensure_future(request(url)) for url in urls]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    end = datetime.datetime.now()
    print('-' * 80)
    print("my pid: %s, parent pid: %s, start at %s, end at %s" % (os.getpid(), os.getppid(), start, end))


if __name__ == "__main__":
    print(datetime.datetime.now())
    print("cpu count:", cpu_count)
    pool = multiprocessing.Pool(cpu_count)

    names = get_names(options.task_num)
    params = [(i, names[i]) for i in range(options.task_num)]

    pool.map(loop_request_wrapper, [params for i in range(cpu_count)])
    pool.close()
    pool.join()
    print(datetime.datetime.now())
