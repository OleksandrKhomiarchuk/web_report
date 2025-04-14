from unittest.mock import patch
import xml.etree.ElementTree as ET
from flask import url_for


def test_report_format_default(client, mock_report_data):
    with client.application.app_context():
        url = url_for('reportapi')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'text/html' in resp.content_type
    data = resp.get_data(as_text=True)
    assert 'BBB' in data
    assert 'Lewis' in data
    assert 'MER' in data
    assert '1' in data

def test_report_format_html(client, mock_report_data):
    with client.application.app_context():
        url = url_for('reportapi', format='html')
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.content_type == 'text/html; charset=utf-8'
    assert b"<html" in resp.data

def test_report_format_json(client, mock_report_data):
    with client.application.app_context():
        url = url_for('reportapi', format='json')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'application/json' in resp.content_type
    data = resp.get_json()
    assert isinstance(data, list)
    assert data[0]['abbreviation'] == 'AAA'
    assert data[0]['name'] == 'Lewis'
    assert data[1]['team'] == 'FER'
    assert data[1]['lap_time'] == '00:01:30'

def test_report_format_xml(client, mock_report_data):
    with client.application.app_context():
        url = url_for('reportapi', format='xml')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'application/xml' in resp.content_type
    data = resp.get_data(as_text=True)
    root = ET.fromstring(data)
    assert root.tag == 'response'
    items = root.findall('item')
    assert len(items) == 2
    assert items[0].find('abbreviation').text == 'AAA'
    assert items[0].find('team').text == 'MER'
    assert items[1].find('abbreviation').text == 'BBB'
    assert items[1].find('team').text == 'FER'


def test_report_order_asc(client, mocker):
    mocker.patch(
        'resource.report_api.get_race_report',
        return_value=[
            {'lap_time': 1},
            {'lap_time': 2}
        ]
    )
    with client.application.app_context():
        url = url_for('reportapi',format='json', order='asc')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'application/json' in resp.content_type
    json_data = resp.get_json()
    assert json_data[0]['lap_time'] == 1
    assert json_data[1]['lap_time'] == 2

def test_report_order_desk(client, mocker):
    mocker.patch(
        'resource.report_api.get_race_report',
        return_value=[
            {'lap_time': 2},
            {'lap_time': 1}
        ]
    )
    with client.application.app_context():
        url = url_for('reportapi', format='json', order='desc')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'application/json' in resp.content_type
    json_data = resp.get_json()
    assert json_data[0]['lap_time'] == 2
    assert json_data[1]['lap_time'] == 1

def test_report_route_no_data(client):
    with patch('resource.report_api.get_race_report', return_value=None):
        with client.application.app_context():
            url = url_for('reportapi')
        resp = client.get(url)
        assert resp.status_code == 404
        assert b"No race data found" in resp.data


def test_report_error(client):
    with patch('resource.report_api.get_race_report', side_effect=Exception("Test error")):
        with client.application.app_context():
            url = url_for('reportapi')
        resp = client.get(url)
        assert resp.status_code == 500
        assert b"Error generating report" in resp.data
