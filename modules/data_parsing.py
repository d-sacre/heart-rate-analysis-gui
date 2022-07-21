from datetime import datetime
import modules.create_dictionary_keys as cdk


def _process_csv_withings(rawData):
    rawDataPreProc = []

    for row in rawData:
        _helperArray=[]
        _helperArray=[row[0],row[1].strip("[]"),row[2].strip("[]")]
        rawDataPreProc.append(_helperArray)

    rawDataPreProc = rawDataPreProc[1:] # remove header

    rawDataConverted = []

    for row in rawDataPreProc:
        _helperArray=[]
        datetimeOBJECT = datetime.fromisoformat(row[0])
        timestamp = datetime.timestamp(datetimeOBJECT)
        _helperArray=[timestamp,float(row[1]), float(row[2])]
        rawDataConverted.append(_helperArray)
        rawDataConverted.sort()

    return rawDataConverted


def formatDataToStandard(rawData,fileType,dataType):
    _dataStandardized = []

    match fileType:
        case "csv":
            match dataType:
                case "withings":
                    _dataStandardized = _process_csv_withings(rawData)

                case _:
                    print("Fatal Error: Data type either not specified or recognized. Aborting.")
        
        case _:
            print("Fatal Error: File type either not specified or recognized. Aborting.")

    return _dataStandardized

# def convertArrayToDict(dataStandardized):
#     _completeDataDICT={}

#     for _entry in dataStandardized:
#         _dt_object = datetime.fromtimestamp(_entry[0])
#         _keyYear = _dt_object.year
#         _keyMonth = _dt_object.month
#         _keyDay = _dt_object.day

#         cdk.checkAndGenerateDictKeys(_completeDataDICT, _keyYear,_keyMonth, _keyDay)

#         _completeDataDICT[_keyYear][_keyMonth][_keyDay].append({"timestamp": _entry[0], "heartRateBPM": _entry[2]})

#     return _completeDataDICT


# def convertDictToPlotArray(dataDICT):
#     _date = []
#     _minimum = []
#     _average = []
#     _maximum = []

#     _keyYearList = list(dataDICT.keys())

#     for _keyYear in _keyYearList:
#         _keyMonthList = list(dataDICT[_keyYear].keys())
#         for _keyMonth in _keyMonthList:
#             _keyDayList = list(dataDICT[_keyYear][_keyMonth].keys())
#             for _keyDay in _keyDayList:
#                 _dateString = str(_keyYear)+"-"+str(_keyMonth)+"-"+str(_keyDay)
#                 _date.append(_dateString)
#                 _minimum.append(dataDICT[_keyYear][_keyMonth][_keyDay]["dailyMin"])
#                 _average.append(dataDICT[_keyYear][_keyMonth][_keyDay]["dailyAvg"])
#                 _maximum.append(dataDICT[_keyYear][_keyMonth][_keyDay]["dailyMax"])

#     return _date, _minimum, _average, _maximum

# def convertTimestampToHoursFromMidnight(timestamp):
#     _now = datetime.fromtimestamp(timestamp)
#     _timeSinceMidnight =  ((_now - _now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())/3600
#     return _timeSinceMidnight

# def convertDictTo24hPlotArray(dataDICT):

#     _keyYearList = list(dataDICT.keys())
#     _completeData = []
#     for _keyYear in _keyYearList:
#         _yearHelper=[]
#         _keyMonthList = list(dataDICT[_keyYear].keys())
#         for _keyMonth in _keyMonthList:
#             _monthHelper = []
#             _keyDayList = list(dataDICT[_keyYear][_keyMonth].keys())
#             for _keyDay in _keyDayList:
#                 dayTimestamp = []
#                 dayHeartRate = []

#                 obj = dataDICT[_keyYear][_keyMonth][_keyDay]

#                 _date = str(_keyYear)+ "-" + str(_keyMonth).zfill(2) + "-" + str(_keyDay).zfill(2)

#                 for i in range(len(obj)):
#                     dayTimestamp.append(parsing.convertTimestampToHoursFromMidnight(obj[i]["timestamp"]))
#                     dayHeartRate.append(obj[i]["heartRateBPM"])

#                 _monthHelper.append([_date,dayTimestamp,dayHeartRate])
            
#             _yearHelper.append(_monthHelper)
#         _completeData.append(_yearHelper)

#     return _completeData
