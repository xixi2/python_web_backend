import os
import asyncio
import requests
import datetime
from tornado.options import define, parse_command_line, options

from utils import get_req_url

define("ip", type=str, default="127.0.0.1")
define("port", type=int, default=8888)
define("api_name", type=str, default="/say/hello")
define("params", type=str, default="name=Lucy")
define("task_num", type=int, default=10)

parse_command_line()


async def request(url):
    status = requests.get(url)
    return status


if __name__ == "__main__":
    print(datetime.datetime.now())
    print("my pid: %s" % (os.getpid()))

    tasks = [asyncio.ensure_future(request(get_req_url(options))) for _ in range(options.task_num)]
    # print("Tasks:", tasks)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    for task in tasks:
        print("Task Result:", task.result())

    print(datetime.datetime.now())
