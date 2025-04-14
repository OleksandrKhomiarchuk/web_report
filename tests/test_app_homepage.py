from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from flask import url_for

def test_favicon(client):
    response = client.get('/favicon.ico')
    assert response.status_code == 200
    assert b"" in response.data

def test_homepage_format_default(client):
    with client.application.app_context():
        url = url_for('homepageapi')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'text/html' in resp.content_type
    soup = BeautifulSoup(resp.get_data(as_text=True), 'html.parser')
    assert soup.html is not None
    assert soup.title is not None
    assert soup.title.string == '\n    2018 Monaco F1 Results\n'
    assert soup.find('h1').text == 'Report of Monaco 2018 Racing'
    h1 = soup.find('h1')
    assert h1 is not None
    assert "Report of Monaco 2018 Racing"   in h1.text
    assert "homepage", "base" in resp.data.decode('utf-8')

def test_homepage_format_html(client):
    with client.application.app_context():
        url = url_for('homepageapi', format='html')
    resp = client.get(url)
    assert resp.status_code == 200
    assert resp.content_type == 'text/html; charset=utf-8'
    assert b"<html" in resp.data

def test_homepage_format_json(client):
    with client.application.app_context():
        url = url_for('homepageapi', format='json')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'application/json' in resp.content_type
    data = resp.get_json()
    assert 'message' in data
    assert 'description' in data
    assert 'version' in data

def test_homepage_format_xml(client):
    with client.application.app_context():
        url = url_for('homepageapi', format='xml')
    resp = client.get(url)
    assert resp.status_code == 200
    assert 'application/xml' in resp.content_type
    data = resp.get_data(as_text=True)
    root = ET.fromstring(data)
    assert root.tag == 'response'
    assert 'message' in data
    assert 'description' in data
    assert 'version' in data

def test_homepage_post_method(client):
    resp = client.post('/')
    assert resp.status_code == 404

def test_homepage_links(client):
    with client.application.app_context():
        url = url_for('homepageapi')
    resp = client.get(url)
    soup = BeautifulSoup(resp.data, 'html.parser')
    links = soup.find_all('a')
    assert any("Racing Report" in link.text for link in links)
    assert any("Drivers List" in link.text for link in links)

def test_homepage_no_error(client):
    with client.application.app_context():
        url = url_for('homepageapi')
    resp = client.get(url)
    soup = BeautifulSoup(resp.data, 'html.parser')
    assert "Error" not in soup.title.text
    assert "404" not in soup.title.text
