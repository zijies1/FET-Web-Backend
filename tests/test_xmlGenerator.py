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

def test_compulsoryXml():
    expected = "<fet version=\"5.39.0\"><Time_Constraints_List><ConstraintBasicCompulsoryTime><Weight_Percentage>100</Weight_Percentage><Active>true</Active><Comments /></ConstraintBasicCompulsoryTime></Time_Constraints_List><Space_Constraints_List><ConstraintBasicCompulsorySpace><Weight_Percentage>100</Weight_Percentage><Active>true</Active><Comments /></ConstraintBasicCompulsorySpace><ConstraintSubjectPreferredRoom><Subject>maths</Subject><Room>B101</Room><Weight_Percentage>50</Weight_Percentage><Active /><Comments /></ConstraintSubjectPreferredRoom><ConstraintSubjectPreferredRoom><Subject>physics</Subject><Room>A101</Room><Weight_Percentage>50</Weight_Percentage><Active /><Comments /></ConstraintSubjectPreferredRoom><ConstraintSubjectPreferredRoom><Subject>chemistry</Subject><Room>B101</Room><Weight_Percentage>50</Weight_Percentage><Active /><Comments /></ConstraintSubjectPreferredRoom></Space_Constraints_List></fet>"
    root = xml.Element("fet", attrib={"version":"5.39.0"})
    data = [{'key': 1, 'room': 'B101', 'subject': 'maths'}, {'key': 11, 'room': 'A101', 'subject': 'physics'}, {'key': 21, 'room': 'B101', 'subject': 'chemistry'}]
    xmlGenerator.compulsoryXml(root, data)
    xml_str = xml.tostring(root).decode()

    assert xml_str == expected
