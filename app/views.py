from flask import request, Response
from flask_cors import CORS
import xml.etree.ElementTree as xml
import json
from helper import *
from app import app

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def hellof():
	return "hello"

@app.route('/api/v1/test', methods=['POST'])
def test():
    # print(request)
    if not request.json:
        return("error")

    data = request.json
    # print(data)
    f = "./" + data["name"] + ".fet"
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
    toXml(data["subjects"]["data"],
          ["Name", "Comments"],
          { "Name": "subject"},
          "Subject",
          children_dic["Subjects_List"])

	# Activity_Tags_List
    toXml(data["tags"]["data"],
          ["Name", "Printable", "Comments"],
          { "Name": "tag"},
          "Activity_Tag",
          children_dic["Activity_Tags_List"])

	#  Teachers_List
    toXml(data["teachers"]["data"],
          ["Name", "Target_Number_of_Hours", "Qualified_Subjects", "Comments"],
          { "Name": "teacher", "Target_Number_of_Hours": "targetNumberOfHours"},
          "Teacher",
          children_dic["Teachers_List"])

	# Students_List
    toXml(data["students"]["data"],
          ["Name", "Number_of_students", "Comments"],
          { "Name": "students", "Number_of_students": "number"},
          "Year",
          children_dic["Students_List"])

	#  Buildings_List
    toXml(data["buildings"]["data"],
          ["Name", "Comments"],
          { "Name": "building" },
          "Building",
          children_dic["Buildings_List"])

	#  Rooms_List
    toXml(data["rooms"]["data"],
          ["Name", "Building", "Capacity", "Comments"],
          { "Name": "room", "Building": "building", "Capacity": "capacity"},
          "Room",
          children_dic["Rooms_List"])

	#  Activities_List
    activityToXml(data["activities"]["data"], children_dic["Activities_List"])

    for key, val in children_dic.items():
        root.append(val)

    # add compulsory constraints
    compulsoryXml(root)
    tree = xml.ElementTree(root)
    with open(f, "wb") as fh:
        tree.write(fh)

    return "hello"
