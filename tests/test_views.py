from app import app
from flask import json
from testData import rawTimetableData
# #from incompleteTestData import rawTimetableData
# def test_hello():
#     response = app.test_client().get('/')
#
#     assert response.status_code == 200
#     assert response.data == b'hello'
#
# def test_generateTimetables():
#     response = app.test_client().post(
#         '/api/v1/test',
#         data=json.dumps(rawTimetableData),
#         content_type='application/json',
#     )
#
#     # check anything goes wrong during the transfromation from json to xml
#     assert response.status_code == 200

# TODO: use fet to test whether the generated xml file is valid or not

# TODO: validate some values in the timetable data files generated by fet