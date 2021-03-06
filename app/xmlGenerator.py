import xml.etree.ElementTree as xml

# hard coded
"""
@data: actual data e.g {"subject": "maths"}
@attributes: tab name fitting .fet format e.g. ["Name", "Comments"]
@values_dic: mapping from actual data to tab name e.g. {"Name":"subject"}
@parentName: name of upper level tab name
             e.g. <parentName><Name>maths</Name></parentName>
"""
def toSingleXml(data, attributes, values_dic, parentName):
    item = xml.Element(parentName)
    for attribute in attributes:
        xmlElement = xml.Element(attribute)
        if attribute in values_dic:
            xmlElement.text = str(data[values_dic[attribute]])
        item.append(xmlElement)
    return item

def toXml(data_list, attributes, values_dic, parentName, parentXml):
    for data in data_list:
        item = toSingleXml(data, attributes, values_dic, parentName)
        if "children" in data:
            for child_data in data["children"]:
                child_item = toSingleXml(child_data, attributes, values_dic, "Group")
                item.append(child_item)
        parentXml.append(item)

def activityToXml(data_list, parentXml):
    mutltiple_attributes = ["Activity_Tag", "Students", "Teacher"]
    child_attributes = ["Duration","Id", "Active", "Comments"]
    parent_attributes = ["Subject", "TotalDuration", "Activity_Group_Id"]
    mutltiple_attributes_dic = {
        "Activity_Tag": "tags",
        "Students": "students",
        "Teacher": "teachers",
    }
    mutltiple_attributes_dic2 = {
        "Activity_Tag": "tag",
        "Students": "students",
        "Teacher": "teacher",
    }
    child_attributes_dic = {
        "Duration": "duration",
        "Id": "key",
        "Active": "active",
    }
    parent_attributes_dic = {
        "Subject": "subject",
        "TotalDuration": "totalDuration",
        "Activity_Group_Id": "key"
    }

    for data in data_list:
        for child in data["children"]:
            item = toSingleXml(data, parent_attributes, parent_attributes_dic, "Activity")
            for attribute in child_attributes:
                xmlElement = xml.Element(attribute)
                if attribute in child_attributes_dic:
                    xmlElement.text = str(child[child_attributes_dic[attribute]])
                item.append(xmlElement)

            for attribute in mutltiple_attributes:
                for element in data[mutltiple_attributes_dic[attribute]]:
                    xmlElement = xml.Element(attribute)
                    xmlElement.text = str(element[mutltiple_attributes_dic2[attribute ]])
                    item.append(xmlElement)
            parentXml.append(item)

"""
 Add compulsory space and time constraints + preferred room constraints
"""
def compulsoryXml(root, data):
    parent_attributes = ["Time","Space"]
    attributes = ["Weight_Percentage","Active","Comments"]
    attributes_dic = {
        "Weight_Percentage":"100",
        "Active":"true",
    }
    for parent_attribute in parent_attributes:
        parentXml = xml.Element("ConstraintBasicCompulsory"+parent_attribute)
        for attribute in attributes:
            xmlElement = xml.Element(attribute)
            if attribute in attributes_dic:
                xmlElement.text = attributes_dic[attribute]
            parentXml.append(xmlElement)
        upperParentXml = xml.Element(parent_attribute+"_Constraints_List")
        upperParentXml.append(parentXml)

        # Add subejct's preferred room constraints
        subject_attributes = ["Subject", "Room"]
        values_dic = {"Subject" : "subject", "Room": "room", "Weight_Percentage": "weight"}
        if(parent_attribute == "Space"):
            for subject in data:
                subject["weight"] = "50"
                item = toSingleXml(
                                    subject,
                                    subject_attributes + attributes,
                                    values_dic,
                                    "ConstraintSubjectPreferredRoom"
                                  )
                upperParentXml.append(item)

        root.append(upperParentXml)
