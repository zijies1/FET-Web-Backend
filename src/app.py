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
        print("error")

    # print(request.json)


    f = "./test.xml"
    root = xml.Element("fet")
    children_list = [
        xml.Element("Institution_Name"),
        xml.Element("Comments"),
        xml.Element("Days_List"),
        xml.Element("Hours_List"),
        xml.Element("Subjects_List"),
        xml.Element("Activity_Tags_List"),
        xml.Element("Teachers_List"),
        xml.Element("Students_List"),
        xml.Element("Activities_List"),
        xml.Element("Buildings_List"),
        xml.Element("Rooms_List")
    ]
    for child in children_list:
        child.text = "testuser"
        root.append(child)
    # print(root)

    tree = xml.ElementTree(root)
    with open(f, "wb") as fh:
        tree.write(fh)

    return "hello"

if __name__ == '__main__':
	# app.run(host='0.0.0.0')
	app.run()
