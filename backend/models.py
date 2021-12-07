from datetime import datetime
from backend import db
from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean


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
    total_clicks = Column(Integer, nullable=False, default=0)


class JobClicks(db.Model):
    __tablename__ = 'job_clicks'

    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False)
    count_clicks = Column(Integer, nullable=False, default=1)
    datetime = Column(DateTime, nullable=False, default=datetime.utcnow())


class ServicesInfo(db.Model):
    __tablename__ = 'services_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String, nullable=False)
    service_type = Column(String)
    run_command = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
