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


