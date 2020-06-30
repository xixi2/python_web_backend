import tornado.ioloop
import tornado.web
import asyncio
import time
import random


class FactorialService(object):  # 定义一个阶乘服务对象

    def __init__(self):
        self.cache = {}  # 用字典记录已经计算过的阶乘

    def calc(self, n):
        if n in self.cache:  # 如果有直接返回
            return self.cache[n]
        s = 1
        for i in range(1, n):
            s *= i
        self.cache[n] = s  # 缓存起来
        return s


class FactorialHandler(tornado.web.RequestHandler):
    service = FactorialService()  # new出阶乘服务对象

    async def get(self):
        n = int(self.get_argument("n"))  # 获取url的参数值
        print("get n = {}".format(n))
        await asyncio.sleep(5)
        self.write(str(self.service.calc(n)))  # 使用阶乘服务
        print("FactorialHandler end")


class SayHelloHanlder(tornado.web.RequestHandler):
    async def get(self):
        name = self.get_argument("name")  # 获取url的参数值
        print("SayHelloHanlder to {}".format(name))
        await asyncio.sleep(3)
        self.write("hello {}".format(name))
        print("SayHelloHanlder end")


class NoParamHandler(tornado.web.RequestHandler):
    def get(self):
        def get_url(handler):
            param_index = handler.request.uri.find('?')
            if param_index == -1:
                return handler.request.uri
            return handler.request.uri[:param_index]

        print("url: %s" % (get_url(self),))
        print("NoParamHandler")


# 注册本模块路由
fact_routing = [
    (r"/fact", FactorialHandler),
    (r"/say/hello", SayHelloHanlder),
    (r"/no/param", NoParamHandler)
]
