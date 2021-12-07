from backend import db
from backend.models import JobClicks, Job


def log_job_click_action(uid: str) -> None:
    job = Job.query.filter(Job.uid == uid).first()
    job.total_clicks += 1
    db.session.add(JobClicks(uid=job.uid))
    db.session.commit()



