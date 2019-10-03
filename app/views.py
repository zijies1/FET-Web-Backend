from flask import request, Response, send_file
from flask_cors import CORS
import xml.etree.ElementTree as xml
from xmljson import badgerfish as bf
from json2xml import json2xml, readfromstring
from json2html import *
from json import dumps
from app import app
from app import xmlGenerator
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
    result = fitOrderToData(data)
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
        finalData = json2html.convert(json = fitDataToHtml(result))

    with open(filePath, "w") as fh:
        fh.write(finalData)
    fh.close()
        # print(fitDataToHtml(result))
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
    print(data)
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
    activityxmlGenerator.toXml(data["activities"]["data"], children_dic["Activities_List"])

    for key, val in children_dic.items():
        root.append(val)

    # add compulsory constraints
    xmlGenerator.compulsoryXml(root, data)
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
        body["subgroups"] = beautifyDays(tmp["Students_Timetable"]["Subgroup"], "teachers", "Teacher")
        # print(beautifyDays(tmp["Students_Timetable"]["Subgroup"], "teachers", "Teacher"))

    with open(prefix + "teachers.xml", "r") as fh:
        # print fh.read()
        tmp = bf.data(xml.fromstring(fh.read()))
        body["teachers"] = beautifyDays(tmp["Teachers_Timetable"]["Teacher"], "students", "Students")
        # print(beautifyDays(tmp["Teachers_Timetable"]["Teacher"], "students", "Students"))

    resp = Response(dumps(body), status=200, mimetype='application/json')
    return resp
    # bad pratice
    # return send_file("../timetables/" + data["name"] + "/" + data["name"] + "_activities.xml")
    #return "hello"

################################ HELPER FUNCTIONS ##############################
def fitOrderToData(json):
    data = json["data"]
    # print(data)
    # print(hourNames)
    dataMap = {}
    for day in data["days"]:
        for hour in day["hours"]:
            dataMap[day["name"] + "_" + str(hour["name"])] = hour
    # print("dataMap => ", dataMap)
    orderedDataList = []
    for key in json["order"]:
        orderedDataList.append(dataMap[key])
    # print(orderedDataList)

    dayCount = 0
    count = 0
    days = []
    dayNames = [x["name"] for x in data["days"]]
    numOfDays = len(dayNames)
    hourNames = [x["name"] for x in data["days"][0]["hours"]]
    # print(dayNames, hourNames)
    for dayName in dayNames:
        newDay = {}
        newDay["name"] = dayName
        newHours = []
        count = 0
        for hourName in hourNames:
            # print(dayCount + count*numOfDays)
            newHour = orderedDataList[dayCount + count*numOfDays]
            newHour["name"] = hourName
            newHours.append(newHour)
            count += 1
        newDay["hours"] = newHours
        days.append(newDay)
        dayCount += 1

    result = {
        "days":days,
        "name":data["name"]
    }
    # print(result)
    return result

def fitDataToHtml(json):
    days = json["days"]
    numOfHours = len(days[0]["hours"])
    newData = []
    for i in range(numOfHours):
        hourRow = {"hour": days[0]["hours"][i]["name"]}
        for day in days:
            if "empty" in day["hours"][i]:
                hourRow[day["name"]]= "empty"
            else:
                finalStr = ""
                for key, value in day["hours"][i].items():
                    if not(key == "name"):
                         if(isinstance(value, list)):
                             for subVal in value:
                                 # print(subVal)
                                 finalStr += (str(subVal["name"]) + " ")
                         else:
                             finalStr += (value + " ")
                hourRow[day["name"]] = finalStr
        newData.append(hourRow)

    return {
        json["name"]: newData
    }

"""
 remove special symbols like @ which is not allowed to be stored in firebase
"""
def beautifyDays(subgroups, unqiueAttributeNew, unqiueAttributeOld):
    result = []
    for subgroup in subgroups:
        days = []
        for day in subgroup["Day"]:
            hours = []
            for hour in day["Hour"]:
                newHour = { "name":hour["@name"]}
                # empty hour
                if(not "Subject" in hour):
                    newHour["empty"] = "true"
                else:
                    print(hour)
                    newHour["subject"] = hour["Subject"]["@name"]
                    try:
                        newHour["activity_tag"] = [ {"name": hour["Activity_Tag"]["@name"]} ]
                    except:
                        newHour["activity_tag"] = [ {"name":x["@name"]} for x in hour["Activity_Tag"]]
                    try:
                        newHour[unqiueAttributeNew] = [ {"name":x["@name"]} for x in hour[unqiueAttributeOld]]
                    except:
                        newHour[unqiueAttributeNew] = [ {"name":hour[unqiueAttributeOld]["@name"]}]
                    try:
                        newHour["room"] = [ {"name": hour["Room"]["@name"] }]
                    except:
                        newHour["room"] = []
                        print("No rooms are being allocated")
                hours.append(newHour)
            newDay = {
                "name":day["@name"],
                "hours":hours
            }
            days.append(newDay)
        newSubgroup = {
            "name":subgroup["@name"],
            "days":days
        }
        result.append(newSubgroup)
    return result
