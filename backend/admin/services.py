import os
import binascii
from backend import db
from typing import List
from datetime import datetime, timedelta
from backend.models import ServicesInfo, JobClicks, Job


def generate_admin_token() -> str:
    return binascii.hexlify(os.urandom(30)).decode()


def get_gathers_info() -> list:
    return sorted([
        {
            'id': service.id,
            'name': service.service_name,
            'type': service.service_type,
            'run_command': service.run_command,
            'is_active': service.is_active
        }
        for service in ServicesInfo.query.all()
    ], key=lambda service: service['id'])


def get_clicks_statistic() -> List[dict]:
    yesterday_datetime = datetime.today() - timedelta(1)

    clicks_info = (
        db.session.query(Job, JobClicks)
        .distinct(Job.uid)
        .join(Job, Job.uid == JobClicks.uid)
        .filter(JobClicks.datetime >= yesterday_datetime)
        .all()
    )
    clicks_info = [models[0] for models in clicks_info]
    return sorted([
        {
            'job_title': job.title,
            'total_clicks': job.total_clicks,
            'uid': job.uid
        }
        for job in clicks_info
    ], key=lambda job: job['total_clicks'], reverse=True)


def run_parsers(parser_id: int) -> None:
    run_command = (
        db.session.query(ServicesInfo.run_command)
        .filter(ServicesInfo.id == parser_id).first()
    )
    if run_command:
        (
            db.session.query(ServicesInfo)
            .filter(ServicesInfo.id == parser_id)
            .update({'is_active': True})
        )
        db.session.commit()
        os.system(f'python -m {run_command[0]}')


def get_total_jobs_in_base() -> int:
    return Job.query.count()
