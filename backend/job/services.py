from backend import db
from backend.models import JobClicks


def log_job_click_action(uid: str) -> None:
    uid_clicks = JobClicks.query.filter(JobClicks.uid == uid).first()

    if bool(uid_clicks):
        uid_clicks.count_clicks += 1
    else:
        db.session.add(JobClicks(uid=uid, count_clicks=1))

    db.session.commit()



