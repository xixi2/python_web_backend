import asyncio
import requests
import datetime
from tornado.options import define, parse_command_line, options

define("ip", type=str, default="127.0.0.1")
define("port", type=int, default=8888)
define("api_name", type=str, default="/say/hello")
define("params", type=int, default="name=Lucy")

parse_command_line()


async def request(url):
    print("request url %s" % (url,))
    status = requests.get(url)
    return status


def callback(task):
    print("in callback, status:", task.result())


def get_req_url():
    ip = options.ip
    port = options.port
    api_name = options.api_name
    params = options.params
    url = "http://%s:%s%s?%s" % (ip, port, api_name, params)
    return url


if __name__ == "__main__":
    print(datetime.datetime.now())
    coroutine = request(get_req_url())
    task = asyncio.ensure_future(coroutine)

    # 当 coroutine 对象执行完毕之后，就去执行声明的 callback() 方法
    task.add_done_callback(callback)
    # print("Task:", task)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    # print("Task:", task)
    print(datetime.datetime.now())
