from flask_restful import Resource
from flasgger import swag_from
from .utils import format_response, render_html, params, get_race_report

class DriversAPI(Resource):
    @swag_from({
        'tags': ['Drivers'],
        'parameters': [
            {
                'name': 'order',
                'in': 'query',
                'type': 'string',
                'default': 'asc',
                'description': 'Sorting order (asc/desc)'
            },
            {
                'name': 'driver_id',
                'in': 'query',
                'type': 'string',
                'required': False,
                'description': 'Driver ID'
            },
            {
                'name': 'format',
                'in': 'query',
                'type': 'string',
                'default': 'html',
                'description': 'Response format (html/json/xml)'}
        ],
        'responses': {
            200: {'description': 'Drivers List or Driver Info'},
            404: {'description': 'No driver data found'},
            500: {'description': 'Error loading drivers:'}
        }
    })

    def get(self):
        """
        API to list of riders.
        Parameters:
        order: The sort order of the list of riders ("asc" or "desc"). Defaults to "asc".
        format: changes page format ("html"/"json"/"xml") default "html".
        driver_id: The ID of the rider (abbreviation).
        Return:
        - An HTML page with the rider information if driver_id is specified and found.
        - An HTML page with the list of riders if driver_id is not specified.
        - A 404 error message if the rider information is not found.
        - A 500 error message if there was an error loading the data.
        """
        order, response_format, driver_id = params()
        try:
            race_report = get_race_report(driver_id)
            if driver_id:
                return driver_info(race_report, response_format, driver_id)
            return driver_list(race_report, response_format)
        except Exception as e:
            return f"Error loading drivers: {e}", 500

def driver_info(race_report, response_format, driver_id):
    """
    Retrieves information for a specific rider.
    Parameters:
    race_report: The report containing rider data.
    response_format: The format in which to return the response.
    driver_id: The ID of the rider (abbreviation).
    Returns:
    - The rider information in the specified format.
    - A 404 error if the rider is not found.
    """
    driver_data = next((d for d in race_report if d["abbreviation"] == driver_id), None)
    if not driver_data:
        return "No driver data found", 404
    if response_format == 'html':
        return render_html("driver_info.html",driver=driver_data)
    return format_response(driver_data, response_format)

def driver_list(race_report, response_format):
    """
    Retrieves a list of all riders.
    Parameters:
    race_report: report containing rider data.
    response_format: format in which to return the response.
    Returns:
    -list of riders in the specified format.
    """
    drivers_list = [{"abbreviation": driver["abbreviation"],
                    "name": driver["name"]}for driver in race_report]
    if response_format == 'html':
        return render_html("drivers.html",drivers=drivers_list)
    return format_response(drivers_list, response_format)
