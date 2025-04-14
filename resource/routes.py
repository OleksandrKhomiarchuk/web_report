from flask_restful import Api
from .homepage_api import HomepageAPI
from .report_api import ReportAPI
from .drivers_api import DriversAPI
from flask import send_from_directory, Blueprint


def reg_resources(api: Api):
    """
    Register all routes
    """
    api.add_resource(HomepageAPI, '/api/v1/')
    api.add_resource(ReportAPI, '/api/v1/report/')
    api.add_resource(DriversAPI, '/api/v1/report/drivers/')

api_bp = Blueprint('api_bp', __name__)
@api_bp.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@api_bp.route('/api/v2/report/app.js')
def app_js():
    return send_from_directory('static', 'app.js')

@api_bp.route('/api/v2/report/')
def spa_report():
    return send_from_directory("static", "index.html")