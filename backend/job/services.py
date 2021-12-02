from backend import db
from backend.models import JobClicks


def log_job_click_action(uid: str) -> None:
    uid_clicks = JobClicks.query(JobClicks.uid == uid).first()

    if bool(uid_clicks):
        uid_clicks.uid += 1
        uid_clicks.commit()
        return

    db.session.add(JobClicks(uid=uid, count_clicks=1))




