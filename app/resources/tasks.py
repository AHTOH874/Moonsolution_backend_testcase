import falcon

from libs import Controller
from libs.schema import load_schema
from libs.auth import auth_required
from schemas.task import CreateTaskManageSchema, UpdateTaskManageSchema, PublicTaskSchema
from models.task import Task


class TasksController(Controller):  # Ресурс задач

    @falcon.before(auth_required)
    def on_get(self, req, resp):  # Получение списка задач
        qs = falcon.uri.parse_query_string(req.query_string)
        try:
            tasks = Task.select().where(Task.user == self.user)
            # TODO: response error to client of incorrect querry string. Example: ?page=10asfafa&count=1654asdf
            if ("page" in qs) and ("count" in qs):
                tasks = tasks.paginate(int(qs["page"]), int(qs["count"]))
            else:
                tasks = tasks.execute()
        except Task.DoesNotExist:
            raise falcon.HTTPBadRequest(description=f'No tasks were found for this user: {self.user.login}')
        except Exception as e:
            print(e)
            falcon.HTTPBadRequest()

        resp.body = PublicTaskSchema(many=True).dumps(tasks)

    @falcon.before(auth_required)
    @load_schema(CreateTaskManageSchema)  # Создание задачи
    def on_post(self, req, resp):
        try:
            Task.get(Task.title == req.parsed['title'], Task.user == self.user)
            raise falcon.HTTPBadRequest(description=f'Task with this title: {req.parsed["title"]} has been founded')
        except Task.DoesNotExist:
            task = Task(title=req.parsed['title'], text=req.parsed['text'], user=self.user,
                        is_important=req.parsed['is_important'] if "is_important" in req.parsed else False)
            task.save()

        resp.body = PublicTaskSchema().dumps(task)

    @falcon.before(auth_required)
    @load_schema(UpdateTaskManageSchema)
    def on_put(self, req, resp):  # Изменение задачи
        if 'text' in req.parsed and 'is_important' in req.parsed:
            task = Task.update(text=req.parsed['text'], is_important=req.parsed['is_important'])
        elif 'is_important' in req.parsed:
            task = Task.update(is_important=req.parsed['is_important'])
        elif 'text' in req.parsed:
            task = Task.update(text=req.parsed['text'])

        try:
            Task.get(Task.title == req.parsed['title'], Task.user == self.user)
            task.where(Task.title == req.parsed['title'], Task.user == self.user).execute()
        except Task.DoesNotExist:
            raise falcon.HTTPNotFound(description=f'No tasks were found with this title: {req.parsed["title"]}')
        except Exception as e:
            print(e)
            raise falcon.HTTPBadRequest()

        raise falcon.HTTPStatus(falcon.HTTP_200, body="Task has been updated.")

    @falcon.before(auth_required)
    @load_schema(UpdateTaskManageSchema)
    def on_delete(self, req, resp):  # Удаление задачи
        try:
            Task.get(Task.title == req.parsed['title'], Task.user == self.user).delete_instance()
        except Task.DoesNotExist:
            raise falcon.HTTPBadRequest(description=f'Task with this title: {req.parsed["title"]} has not founded')

        raise falcon.HTTPStatus(falcon.HTTP_200, body="Task has been deleted.")

