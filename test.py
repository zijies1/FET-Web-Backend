import xml.etree.ElementTree as xml
from xmljson import badgerfish as bf
from json import dumps



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
                    newHour["subject"] = hour["Subject"]["@name"]
                    newHour["activity_tag"] = hour["Activity_Tag"]["@name"]
                    newHour[unqiueAttributeNew] = [ {"name":x["@name"]} for x in hour[unqiueAttributeOld]]
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

   # print dumps(body)

if __name__ == '__main__':
   types = ["subgroups"]
   # types = ["activities", "subgroups", "teachers"]
   id = "test1"
   body = {}

   with open("./test1-single/" + id + "_" + "subgroups.xml", "r") as fh:
       # print fh.read()
       tmp = bf.data(xml.fromstring(fh.read()))
       print(beautifyDays(tmp["Students_Timetable"]["Subgroup"], "teachers", "Teacher"))

   with open("./test1-single/" + id + "_" + "teachers.xml", "r") as fh:
       # print fh.read()
       tmp = bf.data(xml.fromstring(fh.read()))
       print(beautifyDays(tmp["Teachers_Timetable"]["Teacher"], "students", "Students"))
