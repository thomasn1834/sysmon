import os

import tornado.ioloop
import tornado.web

from readfile import main

WEBPATH = os.path.abspath(os.path.dirname(__file__))

class MainHandler(tornado.web.StaticFileHandler):
    pass

class RefreshHandler(tornado.web.RequestHandler):
    def get(self, path):
        if path == "refresh":
            self.write(main())

def make_app():
    return tornado.web.Application([
        (r"/systeminfo/(.+)", RefreshHandler),
        (r"/(.*)", MainHandler, dict(path=WEBPATH, default_filename="Sysmon_v02.html")),
    ])

if __name__ == "__main__":
    port = 8888
    print "listening on port " + str(port)
    app = make_app()
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
