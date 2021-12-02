from backend.models import Job
from backend.schemas.schema import JobSerpSchema
from flask import Blueprint, make_response, jsonify, request


serp = Blueprint('serp', __name__)


@serp.route('/')
def serp_page():
    return make_response(jsonify({'message': 'Jobs page'}), 200)


@serp.route('/get-jobs', methods=['GET', 'POST'])
def get_jobs():
    response = {}
    jobs_per_page = 20
    page_number = int(request.args['page'])
    try:
        jobs = (
            Job.query.order_by(Job.id)
            .offset((page_number - 1) * jobs_per_page)
            .limit(jobs_per_page)
            .all()
        )
        response.update({'jobs': JobSerpSchema().dump(jobs, many=True), 'next_page': bool(jobs)})
    except:
        response.update({'error': "Jobs cannot be obtained"})

    return jsonify(response)



