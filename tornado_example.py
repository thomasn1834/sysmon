from json import loads as jloads

from tornado.ioloop import IOLoop
from tornado.web import (
    RequestHandler,
    Application
)

class AdminHandler(RequestHandler):
    def get(self, action):
        if action == "shutdown":
            print("Shutting down...")
            self.write("Goodbye!")
            self.finish()
            IOLoop.current().stop()
        else:
            res = "Unknown action %s" % action
            print(res)
            self.write(res)
            
class CGIHandler(RequestHandler):
    def get(self, user):
        if user == "Tyler":
            self.write("Welcome back Tyler")
        else:
            self.write("Hi there, %s" % user)
            
def make_app():
    return Application([
        (r"/user/(.+)", CGIHandler),
        (r"/admin/(.+)", AdminHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(9999)
    IOLoop.current().start()
