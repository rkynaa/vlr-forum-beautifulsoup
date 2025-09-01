from datetime import datetime
from utils.datetime_utils import add_zero_leads, reformat_24_to_12, date_remake

def datetime_match(year, datetimeRaw):
    # Match's date
    matchDate = datetimeRaw[0].text.split() # Splitting all parts of the match's date into a list
    matchDateNewLst = date_remake(year, matchDate)

    # Adding zero-leads
    add_zero_leads(matchDateNewLst)

    # Match's time
    matchTime = datetimeRaw[1].text.split()

    # Re-formating the time from 12hr into 24hr
    matchTimeZone = matchTime[-1]
    matchTimeNewLst = reformat_24_to_12(matchTime)
    
    # Adding zero-leads
    add_zero_leads(matchTimeNewLst)

    matchDateNew = "/".join(matchDateNewLst)
    matchTimeNew = ":".join(matchTimeNewLst)
    matchDateTimeFinal = matchDateNew + " " +  matchTimeNew

    return matchDateTimeFinal

def info_match(infoMatchRaw):
    matchInfo = " ".join(infoMatchRaw[0].text.split()).split("|") # Splitting the match's webpage title
    for partMatchInfo in matchInfo: # For each parts of the title
        partMatchInfo = partMatchInfo.strip() # Removing the leading and trailing spaces of each parts
    teamNameLst = [teamName.strip() for teamName in matchInfo[0].split(" vs. ")] # Splitting the team names from part of the title
    matchInfo.pop(0) # Removing the first part of the title list (i.e., Team Heretics vs. Karmine Corp)
    matchInfo.pop(-1) # Removing the last part of the title list (i.e., vlr.gg)
    matchInfo.pop(-1) # Removing the original second last part of the title list (i.e., Valorant Match)
    matchInfo = [partMatchInfo.strip() for partMatchInfo in matchInfo]
    return matchInfo, teamNameLst

def maps_match(mapsMatchRaw, disabledMapsMatchRaw):
    
    mapLst = [] # List of selected maps in the match
    mapLstDisabled = [matchMap.text.split()[1] for matchMap in disabledMapsMatchRaw] # List of unplayed selected maps

    for countMap in range(len(mapsMatchRaw)): # For each maps in the match
        tempLst = mapsMatchRaw[countMap].text.split() # Splitting the text into a list
        if tempLst[1] in mapLstDisabled: # If the map is unplayed,
            continue # Skip the map
        
        if countMap == 0: # If the map is 'All Maps',
            mapLst.append(" ".join(tempLst)) # Add entirety of the text
        else: # If not,
            mapLst.append(tempLst[1]) # Add only the second element of the text, which is the name of the map
        
    mapLst[0], mapLst[1] = mapLst[1], mapLst[0] # Switch the map since the query result shows the map 1 first AND THEN all maps

    return mapLst

def players_match(playersMatchRaw):
    playersLst = [] # Empty list of players in the match
    for matchPlayer in playersMatchRaw: # For each players in the match
        matchPlayerEntry = matchPlayer.text.split()
        playersLst.append(matchPlayerEntry) # Add the player, along with the player's team initials in the list
        # print(matchPlayerEntry) # Check if the entry is correct
    return playersLst