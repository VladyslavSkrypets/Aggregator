from marshmallow import Schema, fields


class GatherJobSchema(Schema):
    id = fields.Int()
    url = fields.Str()
    title = fields.Str()
    region = fields.Str()
    salary = fields.Str()
    job_type = fields.Str()
    company = fields.Str()
    remote_type = fields.Str()
    posted_at = fields.DateTime()
    description = fields.Str()

