def checkAndGenerateDictKeys(dictionary, keyYear, keyMonth, keyDay):
    if keyYear not in list(dictionary.keys()):
        dictionary[keyYear] = {}
    if keyMonth not in list(dictionary[keyYear].keys()):
        dictionary[keyYear][keyMonth] = {}
    if keyDay not in list(dictionary[keyYear][keyMonth].keys()):
        dictionary[keyYear][keyMonth][keyDay] = []