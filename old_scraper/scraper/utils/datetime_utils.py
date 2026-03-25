from datetime import datetime

def add_zero_leads(inpLst):
    for count in range(len(inpLst)):
        if len(inpLst[count]) == 1: # if the number is only have single digit,
            inpLst[count] = "0" + inpLst[count] # it will have zero-leading instead of single digit

def reformat_24_to_12(matchTime):
    matchTimeHour = int(matchTime[0].split(":")[0]) + 12 if matchTime[1].lower() == 'pm' and int(matchTime[0].split(":")[0]) != 12 else int(matchTime[0].split(":")[0])
    # matchTimeHour = matchTimeHour - 12 if matchTimeHour == 24 else matchTimeHour
    matchTime[0] = str(matchTimeHour) + ":" + matchTime[0].split(":")[1]
    matchTimeNewLst = (matchTime[0] + ":00").split(":")

    return matchTimeNewLst

def date_remake(year, matchDate):
     # Splitting all parts of the match's date into a list
    if len(matchDate) == 4 or "," in matchDate[0]:
        matchDate.pop(0) # Removing the day part (i.e., Monday, Tuesday, Wednesday etc.)
    matchDate[0] = matchDate[0][0:3] # Getting the first 3 letter of the month

    matchDay = str(matchDate[1][:-1]) # Getting the date number of the match
    if matchDay[-1] == "s" or matchDay[-1] == "t" or matchDay[-1] == "r" or matchDay[-1] == "n":
        matchDay = matchDay[:-1]
        
    matchMonth = str(datetime.strptime(matchDate[0], '%b').month) # Getting the month number of the match
    matchYear = year # Getting the year number of the match
    matchDateNewLst = [matchYear, matchMonth, matchDay] # Combining the match's date, month and year into a list

    return matchDateNewLst