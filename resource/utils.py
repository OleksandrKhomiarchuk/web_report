import xml.etree.ElementTree as ET
from flask import (Response, make_response,
                   render_template, request, jsonify)
from database.models import Driver, Result


def convert_times_to_str(data):
    if isinstance(data, dict):
        return {k: convert_times_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_times_to_str(item) for item in data]
    return data

def format_response(data, resource_format):
    """
    Formats data in XML or JSON and returns HTTP response.
    :param data: data to serialize (list or dictionary)
    :param resource_format: required format ('json' or 'xml')
    :return: flask response with formatted data
    """
    if resource_format == 'xml':
        root = ET.Element("response")
        dict_to_xml(root, data)
        xml_str = ET.tostring(root, encoding='utf8')
        return Response(xml_str, mimetype='application/xml')
    data = convert_times_to_str(data)
    return jsonify(data)


def dict_to_xml(parent, data):
    """
    Converts a dictionary to XML.
    :param parent: parent XML element (root or sub element)
    :param data: data (dictionary or list)
    :return:
    """
    if isinstance(data, list):
        for item in data:
            child = ET.SubElement(parent, 'item')
            dict_to_xml(child, item)
    elif isinstance(data, dict):
        for key, value in data.items():
            child = ET.SubElement(parent, key)
            child.text = str(value)

def render_html(template_name, **context):
    """
    Universal renders HTML templates
    """
    return make_response(render_template(template_name, content_template="base.html", **context))

def params():
    order = request.args.get('order', "asc")
    response_format = request.args.get('format', "html")
    driver_id = request.args.get('driver_id')
    return order, response_format, driver_id

def get_race_report(order):
    """
    Returns a race report ordered by lap_time.
    :param order: 'asc' for ascending, 'desc' for descending.
    :return: List of race results sorted by lap_time.
    """
    order = Result.lap_time.asc() if order == 'asc' else Result.lap_time.desc()
    query = (Result
             .select(Result, Driver)
             .join(Driver)
             .order_by(order))
    results = []
    for idx, row in enumerate(query, start=1):
        results.append({
            "position": idx,
            "abbreviation": row.driver.abbreviation,
            "name": row.driver.name,
            "team": row.driver.team,
            "date": row.start_time.date(),
            "lap_time": row.lap_time
        })
    return results
