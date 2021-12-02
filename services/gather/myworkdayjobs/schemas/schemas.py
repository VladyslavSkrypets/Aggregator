from services.gather.database import Company, Job
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class CompanySchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = True


class JobSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Job
        load_instance = True


company_schema = CompanySchema(many=True)
job_schema = JobSchema(many=True)

