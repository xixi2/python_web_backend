import os
import asyncio
import requests
import datetime
import multiprocessing
from tornado.options import define, options, parse_command_line
from utils import get_req_url, get_names

define("ip", type=str, default="127.0.0.1")
define("port", type=int, default=8888)
define("api_name", type=str, default="/say/hello")
define("params", type=str, default="name=Lucy")
define("task_num", type=int, default=5)

parse_command_line()


def request(params):
    _, name = params
    kv = "name=%s" % (name,)
    url = get_req_url(options, kv)
    status = requests.get(url)
    print("pid: %s, request url: %s, status: %s" % (os.getpid(), url, status))
    return status


if __name__ == "__main__":
    print(datetime.datetime.now())
    cpu_count = multiprocessing.cpu_count()
    print("cpu count:", cpu_count)  # 当前运行机器上的cpu核数量

    pool = multiprocessing.Pool(cpu_count)

    names = get_names(options.task_num)
    params_list = [(i, names[i]) for i in range(options.task_num)]
    pool.map(request, params_list)
    print(datetime.datetime.now())
