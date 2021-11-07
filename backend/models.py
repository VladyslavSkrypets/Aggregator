from backend import db
from datetime import datetime


class Job(db.Model):
    __tablename__ = 'Job'

    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(), nullable=False, unique=True)
    uid = db.Column(db.String(), nullable=False, unique=True)
    title = db.Column(db.NVARCHAR(), nullable=False)
    region = db.Column(db.NVARCHAR(), nullable=False)
    country = db.Column(db.String())
    company = db.Column(db.String())
    description = db.Column(db.NVARCHAR(), nullable=False)
    date_posted = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    user_clicks = db.Column(db.Integer(), nullable=False, default=0)


