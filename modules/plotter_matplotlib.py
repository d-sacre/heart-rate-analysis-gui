import matplotlib.pyplot as plt
# suppress the warning that too many plots are opened
# spurce: https://stackoverflow.com/questions/27476642/matplotlib-get-rid-of-max-open-warning-output
plt.rcParams.update({'figure.max_open_warning': 0}) 

from datetime import datetime

import modules.convert as convert

showGrid = True

# Matplotlib settings
fig_width_cm = 29.7                               # A4 page
fig_height_cm = 21
inches_per_cm = 1 / 2.54                         # Convert cm to inches
fig_width = fig_width_cm * inches_per_cm         # width in inches
fig_height = fig_height_cm * inches_per_cm       # height in inches
fig_size = [fig_width, fig_height]



def plotHeartRate24hForAllDays(dataARRAY,exportPath):

    global showGrid

    for _year in dataARRAY:
        for _month in _year:
            for _day in _month:
                dayTimestamp = _day[1]
                dayHeartRate = _day[2]
                _date = _day[0]

                fig=plt.figure()
                fig.set_size_inches(fig_size)
                plt.plot(dayTimestamp, dayHeartRate)
                plt.xlabel("time elapsed since midnight (h)")
                plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22,24])
                plt.ylabel("heart rate (bpm)")
                plt.grid(showGrid)
                plt.title("Heart rate during " + _date)
                plt.savefig(exportPath + "heart-rate_" + _date +".pdf")

def plotHeartRateTendency(date, minimum, average, maximum, exportPath):
    _minimumPlot = []
    _maximumPlot = []

    _startDate = date[0]
    _endDate = date[-1]

    global showGrid


    for j in range(len(minimum)): 
        _minimumPlot.append(minimum[j]["heartRateBPM"])
        _maximumPlot.append(maximum[j]["heartRateBPM"])

    fig=plt.figure()
    fig.set_size_inches(fig_size)
    plt.plot(date,_minimumPlot, "-*", color="green")
    plt.plot(date,average, "-o", color="gray")
    plt.plot(date,_maximumPlot, "-x", color="red")
    plt.grid(showGrid)
    plt.legend(["daily minimum", "daily average", "daily maximum"])
    plt.xlabel("date")
    plt.ylabel("heart rate (bpm)")
    plt.xticks(rotation=45)
    plt.title("Daily extrema and average of heart rate from " + _startDate + " to " + _endDate)
    plt.savefig(exportPath + "heart-rate_tendency_" + _startDate + "_" + _endDate + ".pdf")

def generateAndPlotMonthlyHeartRateTendency(dataDICT,exportPath): # plot data for only one month

    _keyYearList = list(dataDICT.keys())

    for _keyYear in _keyYearList:
        _keyMonthList = list(dataDICT[_keyYear].keys())
        for _keyMonth in _keyMonthList:
            _keyDayList = list(dataDICT[_keyYear][_keyMonth].keys())
            _date = []
            _minimum = []
            _average = []
            _maximum = []
            for _keyDay in _keyDayList:
                _dateString = str(_keyYear)+"-"+convert.dictKeyToDateString_mm_dd(_keyMonth,_keyDay)
                _date.append(_dateString)
                _minimum.append(dataDICT[_keyYear][_keyMonth][_keyDay]["dailyMin"])
                _average.append(dataDICT[_keyYear][_keyMonth][_keyDay]["dailyAvg"])
                _maximum.append(dataDICT[_keyYear][_keyMonth][_keyDay]["dailyMax"])

            if len(_date) > 1:
                plotHeartRateTendency(_date, _minimum, _average, _maximum,exportPath)

def plotHeartRateExtremaOverHoursOfDay(date, minimum, maximum, exportPath):
    _minimumPlot = []
    _maximumPlot = []

    _startDate = date[0]
    _endDate = date[-1]

    for j in range(len(minimum)): 
        _minimumPlot.append(convert.TimestampToHoursFromMidnight(minimum[j]["timestamp"]))
        _maximumPlot.append(convert.TimestampToHoursFromMidnight(maximum[j]["timestamp"]))

    numBins = 24

    fig = plt.figure()
    fig.set_size_inches(fig_size)
    plt.hist(_minimumPlot,numBins, edgecolor='black', color='green',alpha=0.8)
    plt.xlabel("time elapsed since midnight (h)")
    plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22,24])
    plt.ylabel("number of global heart rate minima occurences")
    plt.title("Histogram of global heart rate minima occurances over the hours of the day from " + _startDate + " to " + _endDate)

    plt.savefig(exportPath + "heart-rate_global-min-over-hours-of-day_" + _startDate + "_" + _endDate + ".pdf")

    fig = plt.figure()
    fig.set_size_inches(fig_size)
    plt.hist(_maximumPlot,numBins, edgecolor='black', color='red',alpha=0.8)
    plt.xlabel("time elapsed since midnight (h)")
    plt.xticks([0,2,4,6,8,10,12,14,16,18,20,22,24])
    plt.ylabel("number of global heart rate maxima occurences")
    plt.title("Histogram of global heart rate maxima occurances over the hours of the day from " + _startDate + " to " + _endDate)

    plt.savefig(exportPath + "/heart-rate_global-max-over-hours-of-day_" + _startDate + "_" + _endDate + ".pdf")
