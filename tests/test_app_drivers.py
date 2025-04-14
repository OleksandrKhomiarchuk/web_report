from unittest.mock import patch
import xml.etree.ElementTree as ET
from flask import url_for

def test_drivers_list_format_default(client, mock_report_data):
    with client.application.app_context():
        url = url_for('driversapi')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'text/html' in resp.content_type
    data = resp.get_data(as_text=True)
    assert 'Lewis' in data
    assert 'Sebastian' in data

def test_drivers_list_format_html(client, mock_report_data):
    with client.application.app_context():
        url = url_for('driversapi', format='html')
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.content_type == 'text/html; charset=utf-8'
    assert b"<html" in resp.data

def test_drivers_list_format_json(client, mock_report_data):
    with client.application.app_context():
        url = url_for('driversapi', format='json')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'application/json' in resp.content_type
    data = resp.get_json()
    assert isinstance(data, list)
    assert data[0]['abbreviation'] == 'AAA'
    assert data[0]['name'] == 'Lewis'

def test_drivers_list_format_xml(client, mock_report_data):
    with client.application.app_context():
        url = url_for('driversapi', format='xml')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'application/xml' in resp.content_type
    data = resp.get_data(as_text=True)
    root = ET.fromstring(data)
    assert root.tag == 'response'
    items = root.findall('item')
    assert len(items) == 2
    assert items[1].find('abbreviation').text == 'BBB'
    assert items[1].find('name').text == 'Sebastian'

def test_driver_info_format_default(client, mock_report_data):
    with client.application.app_context():
        url = url_for('driversapi', driver_id='AAA')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'text/html' in resp.content_type
    data = resp.get_data(as_text=True)
    assert 'Lewis' in data
    assert 'MER' in data

def test_driver_info_format_html(client, mock_report_data):
    with client.application.app_context():
        url = url_for('driversapi', format='html', driver_id='AAA')
    resp = client.get(url)
    assert resp.content_type == 'text/html; charset=utf-8'
    assert b"<html" in resp.data

def test_driver_info_format_json(client, mock_report_data):
    with client.application.app_context():
        url = url_for('driversapi', format='json', driver_id='BBB')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'application/json' in resp.content_type
    data = resp.get_json()
    assert data['abbreviation'] == 'BBB'
    assert data['name'] == 'Sebastian'
    assert data['team'] == 'FER'
    assert data['lap_time'] == '00:01:30'

def test_driver_info_format_xml(client, mock_report_data):
    with client.application.app_context():
        url = url_for('driversapi', format='xml', driver_id='AAA')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'application/xml' in resp.content_type
    xml_data = resp.get_data(as_text=True)
    root = ET.fromstring(xml_data)
    assert root.tag == 'response'
    assert root.find('abbreviation').text == 'AAA'
    assert root.find('name').text == 'Lewis'
    assert root.find('team').text == 'MER'
    assert root.find('lap_time').text == '00:01:30'

def test_invalid_drivers_with_order_id(client):
    with client.application.app_context():
        url = url_for('driversapi', driver_id='INVALID')
    resp = client.get(url)
    assert resp.status_code == 404
    assert b"No driver data found" in resp.data

def test_drivers_route_error(client):
    with patch('resource.drivers_api.get_race_report', side_effect=Exception("Test error")):
        with client.application.app_context():
            url = url_for('driversapi')
        resp = client.get(url)
        assert resp.status_code == 500
        assert b"Error loading drivers" in resp.data
