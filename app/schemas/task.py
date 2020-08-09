from marshmallow import Schema, fields, validate


class CreateTaskManageSchema(Schema):

    title = fields.String(required=True,
                          validate=validate.Length(max=255))  # See maxLength of string in pewee.CharField
    text = fields.String(required=True,
                         validate=validate.Length(max=255))
    is_important = fields.Boolean(default=False)


class UpdateTaskManageSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(max=255))
    text = fields.String(validate=validate.Length(max=255))
    is_important = fields.Boolean()


class PublicTaskSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    text = fields.String()
    is_important = fields.Boolean()
