import xml.etree.ElementTree as xml

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
