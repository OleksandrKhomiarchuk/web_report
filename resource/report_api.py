from flask_restful import Resource
from flasgger import swag_from
from .utils import format_response, render_html, params, get_race_report

class ReportAPI(Resource):
    @swag_from({
        'tags': ['Race Report'],
        'parameters': [
            {
                'name': 'order',
                'in': 'query',
                'type': 'string',
                'default': 'asc',
                'description': 'Sorting order (asc/desc)'
            },
            {
                'name': 'format',
                'in': 'query',
                'type': 'string',
                'default': 'html',
                'description': 'Response format (html/json/xml)'}
        ],
        'responses': {
            200: {'description': 'Race Report'},
            404: {'description': 'No race data found'},
            500: {'description': 'Error generating report:'}
        }
    })

    def get(self):
        """
        API to overall race report.
        Parameters:
        order: Report sort order ("asc" or "desc"). Defaults to "asc".
        format: changes page format ("html"/"json"/"xml") default "html".
        Returns:
        - HTML page with report if data found.
        - 404 error message if data not found.
        - 500 error message if there was an error generating the report.
        """
        order, response_format, _ = params()
        try:
            race_report = get_race_report(order)
            if not race_report:
                return "No race data found", 404
            if response_format == 'html':
                return render_html("report.html", report=race_report)
            return format_response(race_report, response_format)
        except Exception as e:
            return f"Error generating report: {e}", 500
