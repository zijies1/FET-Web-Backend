from app import helper
from testData import subgroupTeacher,subgroupStudent,fitOrderToDataTestData,fitDataToHtmlTestData
import json

def assertObejct(testResult, expectedResult, attribute):
    for i in range(len(testResult)):
        assert testResult[i]["name"] == expectedResult[i]["name"]
        for j in range(len(testResult[i]["days"])):
            assert testResult[i]["days"][j]["name"] == expectedResult[i]["days"][j]["name"]
            for k in range(len(testResult[i]["days"][j]["hours"])):
                testData = testResult[i]["days"][j]["hours"][k]
                expectedData = expectedResult[i]["days"][j]["hours"][k]
                if(attribute in testData):
                    assert testData[attribute] == expectedData[attribute]
                if("subject" in testData):
                    assert testData["subject"] == expectedData["subject"]
                if("room" in testData):
                    assert testData["room"] == expectedData["room"]


def expectedResultTeacher():
    return [{'name': 'teacher1', 'days': [{'name': 'Monday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'subject': 'chemistry', 'activity_tag': [{'name': 'tag1'}], 'students': [{'name': 2019}], 'room': [{'name': 'B101'}]}, {'name': 10, 'empty': 'true'}, {'name': 11, 'empty': 'true'}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}, {'name': 'Tuesday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'subject': 'chemistry', 'activity_tag': [{'name': 'tag1'}], 'students': [{'name': 2020}], 'room': [{'name': 'B101'}]}, {'name': 11, 'empty': 'true'}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}, {'name': 'Wednesday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'empty': 'true'}, {'name': 11, 'empty': 'true'}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}, {'name': 'Thursday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'empty': 'true'}, {'name': 11, 'empty': 'true'}, {'name': 12, 'subject': 'chemistry', 'activity_tag': [{'name': 'tag1'}], 'students': [{'name': 2019}], 'room': [{'name': 'B101'}]}, {'name': 13, 'subject': 'chemistry', 'activity_tag': [{'name': 'tag1'}], 'students': [{'name': 2020}], 'room': [{'name': 'B101'}]}]}]}, {'name': 'teacher2', 'days': [{'name': 'Monday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'subject': 'maths', 'activity_tag': [{'name': 'tag1'}], 'students': [{'name': 2020}], 'room': [{'name': 'B101'}]}, {'name': 11, 'subject': 'maths', 'activity_tag': [{'name': 'tag1'}], 'students': [{'name': 2019}], 'room': [{'name': 'B101'}]}, {'name': 12, 'empty': 'true'}, {'name': 13, 'subject': 'physics', 'activity_tag': [{'name': 'tag1'}], 'students': [{'name': 2020}], 'room': [{'name': 'A101'}]}]}, {'name': 'Tuesday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'empty': 'true'}, {'name': 11, 'subject': 'physics', 'activity_tag': [{'name': 'tag1'}], 'students': [{'name': 2020}], 'room': [{'name': 'A101'}]}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}, {'name': 'Wednesday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'subject': 'physics', 'activity_tag': [{'name': 'tag1'}], 'students': [{'name': 2019}], 'room': [{'name': 'A101'}]}, {'name': 11, 'empty': 'true'}, {'name': 12, 'empty': 'true'}, {'name': 13, 'subject': 'maths', 'activity_tag': [{'name': 'tag1'}], 'students': [{'name': 2019}], 'room': [{'name': 'B101'}]}]}, {'name': 'Thursday', 'hours': [{'name': 8, 'subject': 'physics', 'activity_tag': [{'name': 'tag1'}], 'students': [{'name': 2019}], 'room': [{'name': 'A101'}]}, {'name': 9, 'empty': 'true'}, {'name': 10, 'empty': 'true'}, {'name': 11, 'empty': 'true'}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}]}]

def expectedResultStudent():
    return [{'name': '2019 Automatic Group Automatic Subgroup', 'days': [{'name': 'Monday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'subject': 'chemistry', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher1'}], 'room': [{'name': 'B101'}]}, {'name': 10, 'empty': 'true'}, {'name': 11, 'subject': 'maths', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher2'}], 'room': [{'name': 'B101'}]}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}, {'name': 'Tuesday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'empty': 'true'}, {'name': 11, 'empty': 'true'}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}, {'name': 'Wednesday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'subject': 'physics', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher2'}], 'room': [{'name': 'A101'}]}, {'name': 11, 'empty': 'true'}, {'name': 12, 'empty': 'true'}, {'name': 13, 'subject': 'maths', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher2'}], 'room': [{'name': 'B101'}]}]}, {'name': 'Thursday', 'hours': [{'name': 8, 'subject': 'physics', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher2'}], 'room': [{'name': 'A101'}]}, {'name': 9, 'empty': 'true'}, {'name': 10, 'empty': 'true'}, {'name': 11, 'empty': 'true'}, {'name': 12, 'subject': 'chemistry', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher1'}], 'room': [{'name': 'B101'}]}, {'name': 13, 'empty': 'true'}]}]}, {'name': '2020 Automatic Group Automatic Subgroup', 'days': [{'name': 'Monday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'subject': 'maths', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher2'}], 'room': [{'name': 'B101'}]}, {'name': 11, 'empty': 'true'}, {'name': 12, 'empty': 'true'}, {'name': 13, 'subject': 'physics', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher2'}], 'room': [{'name': 'A101'}]}]}, {'name': 'Tuesday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'subject': 'chemistry', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher1'}], 'room': [{'name': 'B101'}]}, {'name': 11, 'subject': 'physics', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher2'}], 'room': [{'name': 'A101'}]}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}, {'name': 'Wednesday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'empty': 'true'}, {'name': 11, 'empty': 'true'}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}, {'name': 'Thursday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'empty': 'true'}, {'name': 11, 'empty': 'true'}, {'name': 12, 'empty': 'true'}, {'name': 13, 'subject': 'chemistry', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher1'}], 'room': [{'name': 'B101'}]}]}]}]

def expectedResultFitDataToHtml():
    return {'2019 Automatic Group Automatic Subgroup': [{'hour': 8, 'Monday': 'empty', 'Tuesday': 'physics tag1 teacher2 A101 ', 'Wednesday': 'empty', 'Thursday': 'empty'}, {'hour': 9, 'Monday': 'maths tag1 teacher2 B101 ', 'Tuesday': 'chemistry tag1 teacher1 B101 ', 'Wednesday': 'empty', 'Thursday': 'empty'}, {'hour': 10, 'Monday': 'empty', 'Tuesday': 'empty', 'Wednesday': 'chemistry tag1 teacher1 B101 ', 'Thursday': 'empty'}, {'hour': 11, 'Monday': 'maths tag1 teacher2 B101 ', 'Tuesday': 'physics tag1 teacher2 A101 ', 'Wednesday': 'empty', 'Thursday': 'empty'}, {'hour': 12, 'Monday': 'empty', 'Tuesday': 'empty', 'Wednesday': 'empty', 'Thursday': 'empty'}, {'hour': 13, 'Monday': 'empty', 'Tuesday': 'empty', 'Wednesday': 'empty', 'Thursday': 'empty'}]}

def expectedResultOrder():
    return  [{'name': 'Monday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'subject': 'maths', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher2'}], 'room': [{'name': 'B101'}]}, {'name': 10, 'empty': 'true'}, {'name': 11, 'subject': 'maths', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher2'}], 'room': [{'name': 'B101'}]}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}, {'name': 'Tuesday', 'hours': [{'name': 8, 'subject': 'physics', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher2'}], 'room': [{'name': 'A101'}]}, {'name': 9, 'subject': 'chemistry', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher1'}], 'room': [{'name': 'B101'}]}, {'name': 10, 'empty': 'true'}, {'name': 11, 'subject': 'physics', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher2'}], 'room': [{'name': 'A101'}]}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}, {'name': 'Wednesday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'subject': 'chemistry', 'activity_tag': [{'name': 'tag1'}], 'teachers': [{'name': 'teacher1'}], 'room': [{'name': 'B101'}]}, {'name': 11, 'empty': 'true'}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}, {'name': 'Thursday', 'hours': [{'name': 8, 'empty': 'true'}, {'name': 9, 'empty': 'true'}, {'name': 10, 'empty': 'true'}, {'name': 11, 'empty': 'true'}, {'name': 12, 'empty': 'true'}, {'name': 13, 'empty': 'true'}]}]

"""
testing function which will elimating @ symbols and simplify data
"""
def test_beautifyDays():
    testResultTeacher = helper.beautifyDays(subgroupTeacher,"students", "Students")
    testResultStudent = helper.beautifyDays(subgroupStudent,"teachers", "Teacher")

    assertObejct(testResultStudent, expectedResultStudent(), "teachers")
    assertObejct(testResultTeacher, expectedResultTeacher(), "students")

"""
 testing function which will fit data into html convertale format
"""
def test_fitDataToHtml():
    testResultData = helper.fitDataToHtml(fitDataToHtmlTestData)
    expectedResultData = expectedResultFitDataToHtml()
    testDataList = testResultData['2019 Automatic Group Automatic Subgroup']
    expectedStrData = [json.dumps(data) for data in expectedResultData['2019 Automatic Group Automatic Subgroup']]
    testStrData = [json.dumps(data) for data in testDataList]
    for testData in testStrData:
        assert testData in expectedStrData

"""
 testing function which will order data based on an order list
"""
def test_fitOrderToData():
    # print(fitOrderToDataTestData)
    testResultData = helper.fitOrderToData(fitOrderToDataTestData)
    assert testResultData["days"] == expectedResultOrder()
