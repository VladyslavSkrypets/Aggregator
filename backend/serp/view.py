from backend.models import Job
from backend.schemas.schema import JobSerpSchema
from flask import Blueprint, jsonify, request


serp = Blueprint('serp', __name__)


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
        response.update({
            'jobs': JobSerpSchema().dump(jobs, many=True),
            'is_next_page': len(jobs) == jobs_per_page
        })
    except:
        response.update({'error': "Jobs cannot be obtained"})

    return jsonify(response)



