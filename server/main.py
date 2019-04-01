from data_listener import DataListener
from data_sender import GetAll, GetLatest, WebSocketHandler
from tornado import ioloop, web
import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")

WS_SERVER = config.get("DEFAULT", "WS_SERVER")
WS_PORT = config.getint("DEFAULT", "WS_PORT")


def make_app():
    return web.Application([
        (r"/data/all", GetAll),
        (r"/data/all/bt", GetAll),
        (r"/data/all/wifi", GetAll),

        (r"/data/latest", GetLatest),
        (r"/data/latest/bt", GetLatest),
        (r"/data/latest/wifi", GetLatest),

        (r"/ws", WebSocketHandler),
    ])


if __name__ == "__main__":
    print("Starting the server.")
    app = make_app()
    app.listen(WS_PORT)
    ioloop.IOLoop.current().start()
