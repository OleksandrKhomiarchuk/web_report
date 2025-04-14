from flask_restful import Resource
from flasgger import swag_from
from .utils import format_response, render_html, params


class HomepageAPI(Resource):
    @swag_from({
        'tags': ['Homepage'],
        'parameters': [
            {
                'name': 'format',
                'in': 'query',
                'type': 'string',
                'default': 'html',
                'description': 'Response format (html/json/xml)'
            }
        ],
        'responses': {
            200: {'description': 'Homepage'},
        }
    })

    def get(self):
        """
        Homepage API
        Parameters:
        format: changes page format ("html"/"json"/"xml") default "html"
        """
        _, response_format, _ = params()
        data = {
            'message': '2018 Monaco F1 Results',
            'description': 'Report of Monaco 2018 Racing',
            'version': '1.0',
        }
        if response_format == 'html':
            return render_html("homepage.html")
        return format_response(data, response_format)
