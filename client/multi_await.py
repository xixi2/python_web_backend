import asyncio
import datetime
import aiohttp
from tornado.options import define, parse_command_line, options

define("ip", type=str, default="127.0.0.1")
define("port", type=int, default=8888)
define("api_name", type=str, default="/say/hello")
define("params1", type=str, default="name=Lucy")
define("params2", type=str, default="name=Alice")
define("task_num", type=int, default=10)

parse_command_line()


def get_req_url(options, params):
    ip = options.ip
    port = options.port
    api_name = options.api_name
    url = "http://%s:%s%s?%s" % (ip, port, api_name, params)
    return url


async def request_no_sem(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


async def request(url1, url2):
    await request_no_sem(url1)
    print("finish request %s, start to request %s" % (url1, url2))
    await request_no_sem(url2)


if __name__ == "__main__":
    print(datetime.datetime.now())

    url1, url2 = get_req_url(options, options.params1), get_req_url(options, options.params2)
    tasks = [asyncio.ensure_future(request(url1, url2)) for _ in
             range(options.task_num)]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    print(datetime.datetime.now())
