from app import app
from flask import json
from testData import rawTimetableData

def test_hello():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'hello'

def test_generateTimetables():
    response = app.test_client().post(
        '/api/v1/test',
        data=json.dumps(rawTimetableData),
        content_type='application/json',
    )

    assert response.status_code == 200
