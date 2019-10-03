from app import xmlGenerator
import xml.etree.ElementTree as xml

def test_toSingleXml():
    expected = "<Subject><Name>maths</Name><Comments /></Subject>"
    data = {"subject": "maths"}
    attributes = ["Name", "Comments"]
    values_dic = {"Name":"subject"}
    parentName = "Subject"
    rawXml = xmlGenerator.toSingleXml(data, attributes, values_dic, parentName)
    xml_str = xml.tostring(rawXml).decode()

    assert xml_str == expected
