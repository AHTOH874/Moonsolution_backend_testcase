import falcon

from routing import make_app

server = falcon.API()

server.resp_options.secure_cookies_by_default = False

make_app(server)
