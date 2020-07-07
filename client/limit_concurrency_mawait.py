import asyncio, aiohttp
import datetime
from tornado.options import define, parse_command_line, options

define("ip", type=str, default="127.0.0.1")
define("port", type=int, default=8888)
define("api_name", type=str, default="/say/hello")
define("params1", type=str, default="name=Lucy")
define("params2", type=str, default="name=Alice")
define("task_num", type=int, default=10)
define("con_num", type=int, default=2)

parse_command_line()


def get_req_url(options, params):
    ip = options.ip
    port = options.port
    api_name = options.api_name
    url = "http://%s:%s%s?%s" % (ip, port, api_name, params)
    return url


async def request_sem(url, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()


async def request_no_sem(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.read()


async def send_request(i, url1, url2, semaphore):
    await request_sem(url1, semaphore)
    print("request %s, finish request %s, start to request %s" % (i, url1, url2))
    await request_no_sem(url2)
    print("request %s finished" % (i,))


async def run():
    semaphore = asyncio.Semaphore(options.con_num)  # 限制并发量为con_num
    url1, url2 = get_req_url(options, options.params1), get_req_url(options, options.params2)
    tasks = [send_request(i, url1, url2, semaphore) for i in range(options.task_num)]  # 总共task_num个任务
    await asyncio.wait(tasks)


if __name__ == '__main__':
    print(datetime.datetime.now())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

    print(datetime.datetime.now())
