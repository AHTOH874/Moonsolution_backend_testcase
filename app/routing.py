from resources.index import IndexController
from resources.auth import LoginController, UsersCurrentController, LogoutController, UsersController
from resources.tasks import TasksController


def make_app(app):

    app.add_route('/', IndexController())
    app.add_route('/users', UsersCurrentController())  # GET
    app.add_route('/users/sigin', UsersController())  # POST
    app.add_route('/users/login', LoginController())  # POST
    app.add_route('/users/logout', LogoutController())  # GET
    app.add_route('/tasks', TasksController())  # GET POST PUT DELETE
