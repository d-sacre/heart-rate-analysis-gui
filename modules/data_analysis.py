from datetime import datetime

import scipy
from scipy import signal
import numpy as np

from scipy.signal import find_peaks

import modules.create_dictionary_keys as cdk

def _iterateOverListWithIndexList(dataList,indexList):
    _outputARRAY = []
    for element in indexList:
        _outputARRAY.append(dataList[element])
    return np.asarray(_outputARRAY)

def _calculateMinMaxAvgOfNumpyArray(npArray,timestampList):
    _minIndex = np.argmin(npArray)
    _maxIndex = np.argmax(npArray)
    _odict={"min": {"timestamp": timestampList[_minIndex],"value": np.min(npArray)}, "avg": np.average(npArray), "max": {"timestamp": timestampList[_maxIndex], "value": np.max(npArray)}}

    return _odict

def _calculateGlobalMinMaxAvgOfList(timestampList, rawDataLIST, keyAdditive):
    _keys=[keyAdditive+"Min", keyAdditive+"Avg", keyAdditive+"Max"]
    _npDataHelperArray = np.asarray(rawDataLIST)

    _globalMin = np.min(_npDataHelperArray)
    _globalAverage = np.average(_npDataHelperArray)
    _globalMax = np.max(_npDataHelperArray)
    _globalMinIndex = np.argmin(_npDataHelperArray)
    _globalMaxIndex = np.argmax(_npDataHelperArray)
    _globalMinTimestamp = timestampList[_globalMinIndex]
    _globalMaxTimestamp = timestampList[_globalMaxIndex]

    _odict = { _keys[0]: {"timestamp": _globalMinTimestamp, "heartRateBPM": _globalMin},  _keys[1]: _globalAverage,  _keys[2]: {"timestamp": _globalMaxTimestamp, "heartRateBPM": _globalMax}}
    return _odict

def _generateExtremaTimeValuePairs(timestampList,dataList):
    _oarray=[]
    for i in range(len(timestampList)):
        _oarray.append({"timestamp": timestampList[i], "heartRateBPM": dataList[i]})

    return _oarray

def _generateHeartrateMinMaxAvgAnalysis(timestampList, dataList, keyAdditive):
    _minimaIndexList = scipy.signal.argrelmin(np.asarray(dataList),order=1)[0]
    _maximaIndexList = scipy.signal.argrelmax(np.asarray(dataList),order=1)[0]


    # Commented out for debug
    _minimaList = _iterateOverListWithIndexList(dataList,_minimaIndexList)
    _maximaList = _iterateOverListWithIndexList(dataList,_maximaIndexList)
    _minimaTimestampList = _iterateOverListWithIndexList(timestampList,_minimaIndexList)
    _maximaTimestampList = _iterateOverListWithIndexList(timestampList,_maximaIndexList)
    _minimaDICT = _calculateMinMaxAvgOfNumpyArray(_minimaList,timestampList)
    _maximaDICT = _calculateMinMaxAvgOfNumpyArray(_maximaList,timestampList)

    _minMaxAvgDICT = _calculateGlobalMinMaxAvgOfList(timestampList, dataList, keyAdditive)

    _minimaTimeValueDICT = _generateExtremaTimeValuePairs(_minimaTimestampList, _minimaList)
    _maximaTimeValueDICT = _generateExtremaTimeValuePairs(_maximaTimestampList, _maximaList)

    _extremumDataDICT = {"minima": {"analysis": _minimaDICT, "data": _minimaTimeValueDICT}, "maxima": {"analysis": _maximaDICT, "data": _maximaTimeValueDICT}}
    
    # _minMaxAvgDICT={} # only for debug
    # _extremumDataDICT={} # only for debug

    return _minMaxAvgDICT, _extremumDataDICT

def heartRate_minMaxAvg(dataDICT):

    _heartRateDataDailyAnalysis = {}
    _heartRateDataDailyExtrema = {}

    _keyYearList = list(dataDICT.keys())

    for _keyYear in _keyYearList:
        _keyMonthList = list(dataDICT[_keyYear].keys())
        for _keyMonth in _keyMonthList:
            _keyDayList = list(dataDICT[_keyYear][_keyMonth].keys())
            for _keyDay in _keyDayList:
                _heartRateDataOfDayMinMaxAvg = {}
                _heartRateDataOfDayExtremumDICT = {}
                cdk.checkAndGenerateDictKeys(_heartRateDataDailyAnalysis, _keyYear, _keyMonth, _keyDay)
                cdk.checkAndGenerateDictKeys(_heartRateDataDailyExtrema, _keyYear, _keyMonth, _keyDay)

                _dataOfDay=dataDICT[_keyYear][_keyMonth][_keyDay]
                _timestampsOfDay=[]
                _heartRateDataOfDay=[]

                for entry in _dataOfDay:
                    _timestampsOfDay.append(entry["timestamp"])
                    _heartRateDataOfDay.append(entry["heartRateBPM"])

                _heartRateDataOfDayMinMaxAvg, _heartRateDataOfDayExtraDICT = _generateHeartrateMinMaxAvgAnalysis(_timestampsOfDay,_heartRateDataOfDay,"daily")

                # commented out for debug
                _heartRateDataDailyAnalysis[_keyYear][_keyMonth][_keyDay] = _heartRateDataOfDayMinMaxAvg
                _heartRateDataDailyExtrema[_keyYear][_keyMonth][_keyDay] = _heartRateDataOfDayExtraDICT

    return _heartRateDataDailyAnalysis, _heartRateDataDailyExtrema



                
