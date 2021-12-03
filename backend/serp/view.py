from flask import Blueprint, jsonify, request
from backend.serp.services import SerpConstructor


serp = Blueprint('serp', __name__)


@serp.route('/get-jobs', methods=['POST'])
def get_jobs():
    response = {}
    payload = request.json
    # try:
    serp_constructor = SerpConstructor(payload)
    jobs = serp_constructor.get_jobs()
    response.update({
        'jobs': jobs,
        'is_next_page': len(jobs) == serp_constructor.jobs_per_page
    })
    # except:
    #     response.update({'error': "Jobs cannot be obtained"})

    return jsonify(response)



