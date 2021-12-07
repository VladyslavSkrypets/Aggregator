from backend.models import Job
from backend.schemas.schema import JobPageSchema
from backend.job.services import log_job_click_action
from flask import Blueprint, make_response, jsonify, request


job = Blueprint('job', __name__)


@job.route('/<uid>', methods=['POST', 'GET'])
def job_page(uid):
    response = {}
    try:
        job_data = Job.query.filter(Job.uid == uid).first()
        user_action = request.args.get('utm_source', '') == 'searcher'
        if job_data is not None:
            response.update({
                'message': 'success', 'job': JobPageSchema().dump(job_data), 'status': 200
            })
            if user_action:
                log_job_click_action(uid)
        else:
            response.update({'message': 'Job is not found', 'job': {}, 'status': 404})
    except:
        response.update({'message': 'Something went wrong :( Try later!', 'status': 500})

    return make_response(jsonify(response), response['status'])

