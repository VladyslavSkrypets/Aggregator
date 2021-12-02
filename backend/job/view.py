from backend.models import Job
from backend.schemas.schema import JobPageSchema
from flask import Blueprint, make_response, jsonify


job = Blueprint('job', __name__)


@job.route('/<string:uid>', methods=['POST', 'GET'])
def job_page(uid):
    response = {}
    try:
        job_data = Job.query.filter(Job.uid == uid).first()
        if job_data is not None:
            response.update({
                'message': 'success', 'job': JobPageSchema().dump(job_data), 'status': 200
            })
        else:
            response.update({'message': 'Job is not found', 'job': {}, 'status': 404})
    except:
        response.update({'message': 'Something went wrong :( Try later!', 'status': 500})

    return make_response(jsonify(response), response['status'])

