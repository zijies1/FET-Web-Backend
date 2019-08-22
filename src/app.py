from flask import Flask
from flask import request, Response
from flask_cors import CORS
import xml.etree.ElementTree as xml
import json


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/test/hello', methods=['GET'])
def hellof():
	return "hello"

@app.route('/api/v1/test', methods=['POST'])
def test():
    print(request)
    if not request.json:
        return("error")

    data = request.json
    f = "./test.xml"
    root = xml.Element("fet")
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
    for val in data["subjects"]["data"]:
        name = xml.Element("Name")
        comment = xml.Element("Comments")
        name.text = val["subject"]
        item = xml.Element("Subject")
        item.append(name)
        item.append(comment)
        children_dic["Subjects_List"].append(item)

	# Activity_Tags_List
    for val in data["tags"]["data"]:
        name = xml.Element("Name")
        printable = xml.Element("Printable")
        comment = xml.Element("Comments")
        name.text = val["tag"]
        printable.text = "true"
        item = xml.Element("Activity_Tag")
        item.append(name)
        item.append(printable)
        item.append(comment)
        children_dic["Activity_Tags_List"].append(item)

	# Teachers_List
    for val in data["teachers"]["data"]:
        name = xml.Element("Name")
        tagert_number_of_hours = xml.Element("Target_Number_of_Hours")
        qualified_subjects = xml.Element("Qualified_Subjects")
        comment = xml.Element("Comments")
        name.text = val["teacher"]
        tagert_number_of_hours.text = str(val["targetNumberOfHours"])
        item = xml.Element("Teacher")
        item.append(name)
        item.append(tagert_number_of_hours)
        item.append(qualified_subjects)
        item.append(comment)
        children_dic["Teachers_List"].append(item)

	# Students_List
    for val in data["years"]["data"]:
        name = xml.Element("Name")
        number_of_students = xml.Element("Number_of_students")
        comment = xml.Element("Comments")
        name.text = val["year"]
        number_of_students.text = str(val["number"])
        item = xml.Element("Year")
        item.append(name)
        item.append(number_of_students)
        item.append(comment)
        if "children" in data["years"]["data"]:
            for val2 in data["years"]["data"]["children"]:
                group = xml.Element("Group")
                name = xml.Element("Name")
                number_of_students = xml.Element("Number_of_students")
                number_of_students.text = str(val2["number"])
                comment = xml.Element("Comments")
                name.text = val2["year"]
                group.append(name)
                group.append(number_of_students)
                group.append(comment)
                item.append(group)
        children_dic["Students_List"].append(item)





    for key, val in children_dic.items():
        root.append(val)
    # print(root)

    tree = xml.ElementTree(root)
    with open(f, "wb") as fh:
        tree.write(fh)

    return "hello"

if __name__ == '__main__':
	# app.run(host='0.0.0.0')
	app.run()
