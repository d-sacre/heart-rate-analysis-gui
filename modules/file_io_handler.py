import os
import csv
import json

def checkAndCreateDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def loadFile(FILE, fileType):
    _rawData = []

    # Load the data from file with a procedure depending on file type
    # Remark: match statement requires Python 3.10 or higher 
    match fileType:
        case "csv":
            with open(FILE, newline='') as csvfile:
                _csvObject = csv.reader(csvfile, delimiter=',')

                for row in _csvObject:
                    _rawData.append(row)

        case _:
            print("Fatal Error: File type either not specified or recognized. Aborting.")

    return _rawData

def loadSettingsJSON(FILE):
    with open(FILE) as _json_file:
        _data = json.load(_json_file)
    
    return _data

def createPlotAndDataExportFileStructure(exportPath):
    _exportPathPlotsRoot = exportPath + "plots/"

    _exportPaths = {
        "rawData": exportPath + "rawData/",
        "plotsRoot": _exportPathPlotsRoot,
        "singleDays": _exportPathPlotsRoot + "singleDays/",
        "minMax": _exportPathPlotsRoot + "minMax/",
        "monthlyTendency": _exportPathPlotsRoot + "monthlyTendency/",
    }

    _keys = _exportPaths.keys()

    for _key in _keys:
        checkAndCreateDirectory(_exportPaths[_key])

    return _exportPaths