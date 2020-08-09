import falcon

from libs import Controller
from libs.auth import auth_required, make_session, remove_session
from libs.schema import load_schema
from models.user import User
from schemas.user import UserManageSchema, UserPublicSchema


class UsersController(Controller):   # Ресурс регистрации

    @load_schema(UserManageSchema)
    def on_post(self, req, resp):
        try:
            User.get(User.login == req.parsed['login'])
            raise falcon.HTTPBadRequest(description=f'User with login: {req.parsed["login"]} has been founded')
        except User.DoesNotExist:
            user = User(login=req.parsed['login'])
            user.set_password(password=req.parsed['password'])
            user.save()

        resp.body = UserPublicSchema().dumps(user)
        resp.set_cookie(
            'user_session',
            make_session(
                credential=req.parsed['login'],
                user_data=req.host+req.user_agent,
                user_id=user.id
            ),
            path='/'
        )


class LoginController(Controller):

    @load_schema(UserManageSchema)
    def on_post(self, req, resp):

        try:
            user = User.get(User.login == req.parsed['login'])
        except Exception as e:
            print(e)
            raise falcon.HTTPNotFound(description=f'User with login: {req.parsed["login"]} not found')

        if not user.check_password(req.parsed['password']):
            raise falcon.HTTPUnauthorized(description='Incorrect password')

        resp.body = UserPublicSchema().dumps(user)
        resp.set_cookie(
            'user_session',
            make_session(
                credential=req.parsed['login'],
                user_data=req.host+req.user_agent,
                user_id=user.id
            ),
            path='/'
        )


class UsersCurrentController(Controller):

    @falcon.before(auth_required)
    def on_get(self, req, resp):

        resp.body = UserPublicSchema().dumps(self.user)


class LogoutController(Controller):  # Ресурс разавторизации

    @falcon.before(auth_required)
    def on_get(self, req, resp):
        remove_session(req.cookies['user_session'])
        resp.unset_cookie('user_session')
