from datetime import datetime
from marshmallow import fields, Schema, post_dump


class JobSerpSchema(Schema):
    uid = fields.Str()
    title = fields.Str()
    region = fields.Str()
    job_type = fields.Str()
    company = fields.Str()
    posted_at = fields.DateTime()

    @post_dump
    def prettify_data(self, data, **kwargs):
        data['posted_at'] = datetime.strptime(data['posted_at'], '%Y-%m-%dT%H:%M:%S.%f')
        data['posted_at'] = data['posted_at'].strftime('%b %d, %Y')
        return data


class JobPageSchema(Schema):
    url = fields.Str()
    title = fields.Str()
    region = fields.Str()
    salary = fields.Str()
    job_type = fields.Str()
    company = fields.Str()
    description = fields.Str()

