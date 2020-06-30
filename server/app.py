import tornado.web
import tornado.ioloop
from tornado.options import define, parse_command_line, options

define("port", type=int, default=8888, help="服务端监听的端口")
parse_command_line()

from handlers.fact_handler import fact_routing
from handlers.use_db import use_db_routing


def make_app():
    routings = fact_routing + use_db_routing
    return tornado.web.Application(routings)


if __name__ == "__main__":
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
