from backend import db
from sqlalchemy import Column, String, Integer, DateTime, Text


class Job(db.Model):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    uid = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    region = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    job_type = Column(String, nullable=True)
    company = Column(String, nullable=True)
    remote_type = Column(String(1), nullable=True)
    posted_at = Column(DateTime, nullable=True)
    description = Column(Text, nullable=False)


class JobClicks(db.Model):
    __tablename__ = 'job_clicks'

    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False, unique=True)
    count_clicks = Column(Integer, nullable=False)
