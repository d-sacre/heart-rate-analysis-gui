import sys

import modules.file_io_handler as fio
import modules.data_parsing as parsing
import modules.convert as convert
import modules.data_analysis as analysis
import modules.plotter_matplotlib as plot

def dataProcessingExportingAndPlotting(FILE,EFOLDER):
    
    print("Loading settings")
    settings = fio.loadSettingsJSON("./settings/analysis_settings.json")
    settings["import"]["filepath"] = FILE
    settings["export"]["directory"] = EFOLDER

    # Loading, parsing and pre-processing of data
    print("Importing data and parsing it")
    importedData = fio.loadFile(settings["import"]["filepath"],settings["import"]["datatype"])
    rawDataStandardized = parsing.formatDataToStandard(importedData,settings["import"]["datatype"],settings["import"]["dataformat"])
    completeRawDataDictionary = convert.ArrayToDict(rawDataStandardized)

    # Perform data analysis
    print("Data analysis")
    heartRateDataDailyAnalysis, heartRateDataDailyExtrema = analysis.heartRate_minMaxAvg(completeRawDataDictionary)

    # Convert data into more suitable format for plotting/(raw) data export
    print("Data export preparation")
    date, minimum, average, maximum = convert.DictToPlotArray(heartRateDataDailyAnalysis) 
    completeRawData24hPlotArray = convert.DictTo24hPlotArray(completeRawDataDictionary)

    # Init export folders
    exportPaths = fio.createPlotAndDataExportFileStructure(settings["export"]["directory"])

    # Plot the data
    print("Plot export")
    plot.plotHeartRate24hForAllDays(completeRawData24hPlotArray,exportPaths["singleDays"])
    plot.plotHeartRateExtremaOverHoursOfDay(date, minimum, maximum, exportPaths["minMax"])
    plot.generateAndPlotMonthlyHeartRateTendency(heartRateDataDailyAnalysis,exportPaths["monthlyTendency"])

    print("Analysis finished successfully!")
    