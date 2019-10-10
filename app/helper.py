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
    print("subgroups",subgroups, unqiueAttributeNew, unqiueAttributeOld)
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
