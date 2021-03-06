from app import app
from app import helper
from test_helper import assertObejct
from flask import json
from testData import rawTimetableData
import xml.etree.ElementTree as xml
import subprocess
from xmljson import badgerfish as bf


"""
test hello world API
"""
def test_helloAPI():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert response.data == b'hello'

"""
test generate timetables API
"""
def test_generateTimetablesAPI():
    response = app.test_client().post(
        '/api/v1/test',
        data=json.dumps(rawTimetableData),
        content_type='application/json',
    )

    # check anything goes wrong during the transfromation from json to xml
    assert response.status_code == 200

"""
use fet to test whether the generated xml file is valid or not
and validate some values in the timetable data files generated by fet
"""
def test_fet():
    stdoutdata = subprocess.getoutput("sudo fet-cl --inputfile=test.fet")
    # wheter fet generator goes well
    assert stdoutdata.splitlines()[-1] == "Simulation successful"

    prefix = "./timetables/test/test_"
    with open(prefix + "subgroups.xml", "r") as fh:
        tmp = bf.data(xml.fromstring(fh.read()))
        testResultStudent = helper.beautifyDays(tmp["Students_Timetable"]["Subgroup"], "teachers", "Teacher")
        # validate some values in the timetable data files generated by fet
        assert testResultStudent[0]['name'] == "2019 Automatic Group Automatic Subgroup"
        assert testResultStudent[0]['days'][0]['hours'][0]['name'] == 8
        assert testResultStudent[0]['days'][0]['hours'][1]['name'] == 9
        assert testResultStudent[0]['days'][0]['hours'][2]['name'] == 10
        assert testResultStudent[0]['days'][0]['hours'][3]['name'] == 11

    stdoutdata = subprocess.getoutput("sudo rm -rf ./timetables/test")
