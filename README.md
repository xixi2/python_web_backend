基于tornado开发了一个服务器的例子。并通过该例子说明，协程、事件循环、多进程等概念。最后结合上述所有的东西完成一个小例子。



# 服务端

`app.py`是服务端的入口。执行app.py即启动服务端。
在app.py中启动一个事件循环，监听来自客户端的请求。

```python
import tornado.web
import tornado.ioloop
from tornado.options import define, parse_command_line, options

define("port", type=int, default=8888, help="服务端监听的端口")
parse_command_line()

from handlers.fact import fact_routing
from handlers.use_db import use_db_routing


def make_app():
    routings = fact_routing + use_db_routing
    return tornado.web.Application(routings)


if __name__ == "__main__":
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
```

除了app.py，服务端还有handler文件夹中的多个不同模块的handler.py文件，在这些handler.py中定义了多个handler，对具体客户端的请求进行响应。其他文件的内容具体见代码。

启动服务端

```shell
python3 app.py --port=9999 
```

根据端口号查询服务端进程：

```shell
lsof -i :8888
```

通过curl请求服务端的服务：

```shell
curl http://127.0.0.1:9999/say/hello?name=alice
```

在服务端可以看到：

```shell
xixi2$ python3 app.py --port=9999
SayHelloHanlder to alice
SayHelloHanlder end
[I 200629 23:58:52 web:2246] 200 GET /say/hello?name=alice (127.0.0.1) 1005.81ms
```



# 客户端

在client文件夹有多个py文件，分别以不同的方式对服务端的服务进行了请求。

## `single_task`

以同步方式发送单个请求。使用的http客户端为requests。
在`single_task.py`中请求服务端的`say/hello`接口，而该接口，在运行过程中会睡眠3秒。所以，客户端收到服务端的响应至少需要3秒。

运行结果如下：

```shell
client xixi2$ python3 single_task.py --port=9999
2020-06-30 08:37:45.293302
request url http://127.0.0.1:9999/say/hello?name=Lucy
in callback, status: <Response [200]>
2020-06-30 08:37:48.308382
```

从运行结果可以看出，运行时间大约3秒。







# 参考文献

1. http客户端评测：https://juejin.im/post/5e26f930f265da3e27290e19

