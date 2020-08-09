from marshmallow import Schema, fields


class UserManageSchema(Schema):

    login = fields.String(required=True)
    password = fields.String(required=True)


class UserPublicSchema(Schema):

    id = fields.Integer()
    login = fields.String()
    created_at = fields.DateTime()
