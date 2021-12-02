import datetime
from services.config import GatherDatabase
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


gather_db = GatherDatabase
engine = create_engine(f"postgresql://{gather_db.USER}:{gather_db.PASSWORD}@localhost:{gather_db.PORT}/{gather_db.DATABASE}",
                       poolclass=StaticPool,
                       echo=False)
session = sessionmaker(bind=engine)
Base = declarative_base()


def db_insert_one(db, table, data, lock) -> None:
    try:
        lock.acquire(True)
        db.add(table(**data))
        db.commit()
        db.close()
    finally:
        lock.release()


def db_insert_many(db, data_list, lock) -> None:
    try:
        lock.acquire(True)
        db.add_all(data_list)
        db.commit()
        db.close()
    finally:
        lock.release()


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    domain = Column(String)
    serp_json_url = Column(String)
    serp_category = Column(String)
    jobs_count = Column(Integer)
    expire_at = Column(DateTime, default=(datetime.datetime.utcnow() + datetime.timedelta(days=7)))

    def __init__(self, company_name: str, domain: str, serp_json_url: str, serp_category: str, jobs_count: int):
        self.company_name = company_name
        self.domain = domain
        self.serp_json_url = serp_json_url
        self.serp_category = serp_category
        self.jobs_count = jobs_count


class Job(Base):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    region = Column(String, nullable=True)
    salary = Column(String, nullable=True)
    job_type = Column(String, nullable=True)
    company = Column(String, nullable=True)
    remote_type = Column(String(1), nullable=True)
    posted_at = Column(DateTime, nullable=True)
    description = Column(Text, nullable=False)

    def __init__(self, url: str, title: str, region: str, salary: str, company: str, remote_type: str, job_type: str,
                 posted_at: str, description: str):
        self.url = url
        self.title = title
        self.region = region
        self.company = company
        self.salary = salary
        self.remote_type = remote_type
        self.job_type = job_type
        self.posted_at = posted_at
        self.description = description


def init_db():
    Base.metadata.create_all(engine)
    db = session()
    return db
