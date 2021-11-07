from backend import app, config
from flask import jsonify, make_response
from job.view import job as job_blueprint
from serp.view import serp as serp_blueprint
from admin.view import admin as admin_blueprint


app.register_blueprint(job_blueprint, url_prefix='/job')
app.register_blueprint(serp_blueprint, url_prefix='/jobs')
app.register_blueprint(admin_blueprint, url_prefix='/api/admin')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Not Found!'}), 404)


@app.route("/")
def home():
    return "Hello world"


if __name__ == '__main__':
    app.run(port=config['APP_PORT'])
