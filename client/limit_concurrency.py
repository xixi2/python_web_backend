import asyncio, aiohttp
import datetime
from tornado.options import define, parse_command_line, options

from utils import get_req_url

define("ip", type=str, default="127.0.0.1")
define("port", type=int, default=8888)
define("api_name", type=str, default="/say/hello")
define("params", type=str, default="name=Lucy")
define("task_num", type=int, default=10)
define("con_num", type=int, default=2)

parse_command_line()


async def hello(url, semaphore):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()


async def run():
    semaphore = asyncio.Semaphore(options.con_num)  # 限制并发量为每次con_num个协程
    tasks = [hello(get_req_url(options), semaphore) for _ in range(options.task_num)]  # 总共task_num个任务
    await asyncio.wait(tasks)


if __name__ == '__main__':
    print(datetime.datetime.now())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()

    print(datetime.datetime.now())
