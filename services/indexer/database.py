from services.config import ProductionDatabase
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


prod_db = ProductionDatabase
engine = create_engine(f"postgresql://{prod_db.USER}:{prod_db.PASSWORD}@localhost:{prod_db.PORT}/{prod_db.DATABASE}",
                       poolclass=StaticPool,
                       echo=False)
session = sessionmaker(bind=engine)
Base = declarative_base()


class Job(Base):
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


class ServicesInfo(Base):
    __tablename__ = 'services_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String, nullable=False)
    service_type = Column(String)
    run_command = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)


def init_prod_db():
    Base.metadata.create_all(engine)
    db = session()
    return db
