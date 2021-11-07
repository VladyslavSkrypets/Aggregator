from backend.models import Job
from flask import Blueprint, make_response, jsonify


job = Blueprint('job', __name__)


@job.route('/<int:uid>')
def job_page(uid):
    job_uid = Job.query.filter(uid=uid).first()
    if job_uid:
        return make_response(jsonify({'message': 'job data'}), 200)
    return make_response(jsonify({'message': f'Job page {uid}'}))
