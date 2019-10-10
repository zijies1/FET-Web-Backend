from flask import request, Response, send_file
from flask_cors import CORS
import xml.etree.ElementTree as xml
from xmljson import badgerfish as bf
from json2xml import json2xml, readfromstring
from json2html import *
from json import dumps
from app import app
from app import xmlGenerator
from app import helper
import os

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/printDir', methods=['GET'])
def printDir():
   #print(os.getcwd())
    #os.system("fet-cl --inputfile=test1.fet")
    # print(os.system("tree . "))
    #dir = os.getcwd()
    #print("currentDir => ")
    # print(os.getcwd())
    return os.getcwd()

@app.route('/', methods=['GET'])
def hello():
    return "hello"

@app.route('/api/v1/exportTimetable', methods=['POST'])
def exportTimetable():
    # print(request)
    if not request.json:
        return("error")

    data = request.json
    result = helper.fitOrderToData(data)
    # print("\n\n", data, "\n\n", result)
    # return "hello"

    id = data["key"]
    filePath = "./finalResult/" + id + "/" + id + "." + data["fileType"]
    if not os.path.exists(os.path.dirname(filePath)):
        try:
            os.makedirs(os.path.dirname(filePath))
        except OSError as exc: # Guard against race condition
            return("error")

    finalData = ""
    if(data["fileType"] == "xml"):
        jsonData = readfromstring(dumps(result))
        finalData = json2xml.Json2xml(jsonData).to_xml()
    elif(data["fileType"] == "html"):
        finalData = json2html.convert(json = helper.fitDataToHtml(result))

    with open(filePath, "w") as fh:
        fh.write(finalData)
    fh.close()
        # print(helper.fitDataToHtml(result))
        # return "hello"

    # body = {
    #     "fileType":data["fileType"],
    #     "name":result["name"],
    #     "data":finalData
    # }
    # resp = Response(dumps(body), status=200, mimetype='application/json')

    # print(data)
    return send_file("." + filePath)

@app.route('/api/v1/test', methods=['POST'])
def generateTimetables():
    # print(request)
    if not request.json:
        return("error")

    data = request.json
    # print(data)
    f =  data["key"] + ".fet"
    root = xml.Element("fet", attrib={"version":"5.39.0"})
    children_dic = {
        "Institution_Name":xml.Element("Institution_Name"),
        "Comments":xml.Element("Comments"),
        "Days_List":xml.Element("Days_List"),
        "Hours_List":xml.Element("Hours_List"),
        "Subjects_List":xml.Element("Subjects_List"),
        "Activity_Tags_List":xml.Element("Activity_Tags_List"),
        "Teachers_List":xml.Element("Teachers_List"),
        "Students_List":xml.Element("Students_List"),
        "Activities_List":xml.Element("Activities_List"),
        "Buildings_List":xml.Element("Buildings_List"),
        "Rooms_List":xml.Element("Rooms_List")
    }
	#Institution_Name
    children_dic["Institution_Name"].text = data["name"]

	#Days_List
    number_of_days = xml.Element("Number_of_Days")
    # print(data["days"], len(data["days"]))
    number_of_days.text = str(len(data["days"]))
    children_dic["Days_List"].append(number_of_days)
    for day in data["days"]:
        name = xml.Element("Name")
        name.text = day
        item = xml.Element("Day")
        item.append(name)
        children_dic["Days_List"].append(item)

	# Hours_List
    number_of_hours = xml.Element("Number_of_Hours")
    number_of_hours.text = str(data["numberOfPeriodsPerDay"])
    children_dic["Hours_List"].append(number_of_hours)
    for key, val in data["periods"].items():
        name = xml.Element("Name")
        name.text = val
        item = xml.Element("Hour")
        item.append(name)
        children_dic["Hours_List"].append(item)

	# Subjects_List
    xmlGenerator.toXml(data["subjects"]["data"],
          ["Name", "Comments"],
          { "Name": "subject"},
          "Subject",
          children_dic["Subjects_List"])

	# Activity_Tags_List
    xmlGenerator.toXml(data["tags"]["data"],
          ["Name", "Printable", "Comments"],
          { "Name": "tag"},
          "Activity_Tag",
          children_dic["Activity_Tags_List"])

	#  Teachers_List
    xmlGenerator.toXml(data["teachers"]["data"],
          ["Name", "Target_Number_of_Hours", "Qualified_Subjects", "Comments"],
          { "Name": "teacher", "Target_Number_of_Hours": "targetNumberOfHours"},
          "Teacher",
          children_dic["Teachers_List"])

	# Students_List
    xmlGenerator.toXml(data["students"]["data"],
          ["Name", "Number_of_students", "Comments"],
          { "Name": "students", "Number_of_students": "number"},
          "Year",
          children_dic["Students_List"])

	#  Buildings_List
    xmlGenerator.toXml(data["buildings"]["data"],
          ["Name", "Comments"],
          { "Name": "building" },
          "Building",
          children_dic["Buildings_List"])

	#  Rooms_List
    xmlGenerator.toXml(data["rooms"]["data"],
          ["Name", "Building", "Capacity", "Comments"],
          { "Name": "room", "Building": "building", "Capacity": "capacity"},
          "Room",
          children_dic["Rooms_List"])

	#  Activities_List
    xmlGenerator.activityToXml(data["activities"]["data"], children_dic["Activities_List"])

    for key, val in children_dic.items():
        root.append(val)

    # add compulsory constraints
    xmlGenerator.compulsoryXml(root, data["subjects"]["data"])
    tree = xml.ElementTree(root)
    with open(f, "wb") as fh:
        tree.write(fh)


   # TODO: check whether this goes well
    os.system("fet-cl --inputfile=" + f)

    id = data["key"]
    body = {}
    prefix = "./timetables/" + id  + "/" + id + "_"
    with open(prefix + "subgroups.xml", "r") as fh:
        # print fh.read()
        tmp = bf.data(xml.fromstring(fh.read()))
        # print(tmp["Students_Timetable"]["Subgroup"])
        body["subgroups"] = helper.beautifyDays(tmp["Students_Timetable"]["Subgroup"], "teachers", "Teacher")
        # print(helper.beautifyDays(tmp["Students_Timetable"]["Subgroup"], "teachers", "Teacher"))

    with open(prefix + "teachers.xml", "r") as fh:
        # print fh.read()
        tmp = bf.data(xml.fromstring(fh.read()))
        body["teachers"] = helper.beautifyDays(tmp["Teachers_Timetable"]["Teacher"], "students", "Students")
        # print(helper.beautifyDays(tmp["Teachers_Timetable"]["Teacher"], "students", "Students"))

    resp = Response(dumps(body), status=200, mimetype='application/json')
    return resp
    # bad pratice
    # return send_file("../timetables/" + data["name"] + "/" + data["name"] + "_activities.xml")
    #return "hello"
