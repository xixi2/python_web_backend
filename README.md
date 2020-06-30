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

## `multi_taks_sync`

以同步方式发送10个请求。同时，在这里加入了协程，希望可以利用协程来更好地利用CPU。但是，不幸的是，使用同步请求方式，当请求发送后，在等待服务端响应时，由于等待IO，客户端进程会被挂起。

运行结果

```shell
client xixi2$ python3 multi_task_sync.py --port=9999
2020-06-30 08:56:48.188272
my pid: 4940
Task Result: <Response [200]>
Task Result: <Response [200]>
Task Result: <Response [200]>
Task Result: <Response [200]>
Task Result: <Response [200]>
Task Result: <Response [200]>
Task Result: <Response [200]>
Task Result: <Response [200]>
Task Result: <Response [200]>
Task Result: <Response [200]>
2020-06-30 08:57:18.285911
```

当客户端发送请求后，服务端响应前查看进程状态：

```shell
client xixi2$ ps aux | grep 4940 | grep -v "grep"
xixi2 4940 0.0 0.3 4277384 24296 s001 S+ 8:56 0:00.22 /Python multi_task_sync.py --port=9999
```

可以看出，进程被阻塞，等待IO完成。

因此，在此处加入协程和事件循环无异于画蛇添足，毫无用处。



## `mult_task_async`

要想让协程真正发挥作用，必须让当服务端未返回时，客户端继续发送下一个请求，当收到服务端的响应时，再去处理服务端的响应数据。这就需要异步IO。



## ``





# 参考文献

1. http客户端评测：https://juejin.im/post/5e26f930f265da3e27290e19

