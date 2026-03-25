from datetime import datetime
import time
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
        
        if countMap == 0: # If the map is 'All Maps',
            mapLst.append(" ".join(tempLst)) # Add entirety of the text
        else: # If not,
            mapLst.append(tempLst[1]) # Add only the second element of the text, which is the name of the map

        if tempLst[1] in mapLstDisabled: # If the map is unplayed,
            mapLst.reverse()
            mapLst.remove(tempLst[1])
            mapLstDisabled.remove(tempLst[1])
            mapLst.reverse()
        
    mapLst[0], mapLst[1] = mapLst[1], mapLst[0] # Switch the map since the query result shows the map 1 first AND THEN all maps

    return mapLst

def players_match(playersMatchRaw):
    playersLst = [] # Empty list of players in the match
    for matchPlayer in playersMatchRaw: # For each players in the match
        matchPlayerEntry = matchPlayer.text.split()
        playersLst.append(matchPlayerEntry) # Add the player, along with the player's team initials in the list
    return playersLst

def add_stat_nums_into_non_main_lst(matchStatsRaw, statNumLst, statNumLst_raw, statSideInd, sizeStats):
    join_str = " " if sizeStats == 12 else ""
    
    # Adding the stat numbers
    for queryMatchStat in matchStatsRaw: # for each query result of the match stat
        textTag = join_str.join(queryMatchStat.text.split()).replace("/", "") # Removing the '/' part of the stat, to get the necessary part
        if sizeStats == 12:
            textTag = textTag.split()
        if textTag == "".join(statSideInd): # If the result text tag is empty,
            continue # Skip the stat
        else: # If actually contains a stat,
            if sizeStats == 12:
                if len(textTag) == 5: # If there's a leading and trailing spaces in the text tag,
                    textTag = textTag[1:-1] # Removed the leading and trailing spaces in the text tag
            statNumLst_raw.append(textTag) # Add the stat into the raw list of stat numbers

    for countStatNum_raw in range(0, len(statNumLst_raw), sizeStats): # For each 12 numbers in the raw list
        tempLst = [] # Empty temporary stats List
        for countStat in range(sizeStats): # for each stat in the 12 numbers of stats
            tempLst.append(statNumLst_raw[countStatNum_raw+countStat]) # Add each stats
        statNumLst.append(tempLst) # Add the temporary stats list into the list of stats numbers


def detect_diff_map(matchTeamsLst, mapLst, statSidedLst = None, playersLst = None):
    teamPlayerLst = {i:0 for i in matchTeamsLst}
    countMapPlayed = 0
    rangeLst = statSidedLst.copy() if statSidedLst else playersLst.copy()
    for countLst in range(len(rangeLst)):
        playerTeam = rangeLst[countLst][-1]
        playerTeam = rangeLst[countLst][-1]
        if playerTeam != rangeLst[countLst-1][-1]\
            and teamPlayerLst[rangeLst[countLst-1][-1]] != 0\
                and teamPlayerLst[playerTeam] != 0\
                    and countLst != 0\
                        and countLst != len(rangeLst):
            countMapPlayed += 1
            teamPlayerLst[playerTeam] = 0
            teamPlayerLst[rangeLst[countLst-1][-1]] = 0
        teamPlayerLst[playerTeam] += 1
        rangeLst[countLst].insert(1, mapLst[countMapPlayed])
        if statSidedLst:
            if '+' in rangeLst[countLst][8]:
                rangeLst[countLst][8] = rangeLst[countLst][8][1]
        if '+' in rangeLst[countLst][-2]:
            rangeLst[countLst][-2] = rangeLst[countLst][-2][1]

def get_match_scores(matchScoreRaw):

    matchScores = []
    for countScore in range(len(matchScoreRaw)):
        matchTeamScore = int(matchScoreRaw[countScore].text.strip())
        matchScores.append(matchTeamScore)
    
    return matchScores


def stat_with_sides(statSidedLst_imp, statSidedLst_extra, matchStatsRaw, matchScoresRaw, statNumLst, statNumLst_raw, statSideInd, playersLst, mapLst, teamNameLst, matchInfo, urlMatch, matchDateTime):
    
    num_stats_extra = 12

    # Adding the stat numbers
    add_stat_nums_into_non_main_lst(matchStatsRaw, statNumLst, statNumLst_raw, statSideInd, num_stats_extra)

    for countPlayer in range(len(playersLst)): # For each player in the player list
        playersLst[countPlayer].extend(statNumLst[countPlayer]) # Each player's list got extended with the stat numbers' list

    statSidedLst = [] # Empty list of stats with sides

    sides = ['All', 'Atk', 'Def'] # Each sides in a match (including 'All')

    matchTeamsLst = [] # Empty list of teams in the match

    for countPlayer in range(len(playersLst)): # For each player in the match
        for countSide in range(3): # For each side the player played in
            tempLst = [] # Temporary Empty List to store the proper format of the player stats
            tempLst.append(playersLst[countPlayer][0]) # Add the player's name into the temp list
            tempLst.append(sides[countSide]) # Add the side of the player played in into the temp list
            for countStat in range(2, len(playersLst[0]), 1): # For each stat in the player's list, EXCEPT the player's name and team name
                if len(playersLst[countPlayer][countStat]) < 3: # If the stat is INCOMPLETE (missing stat numbers),
                    while len(playersLst[countPlayer][countStat]) != 3: # While the stat is not complete yet,
                        playersLst[countPlayer][countStat].append('-') # Fill the empty part of the list with '-' to be easily filtered
                tempLst.append(playersLst[countPlayer][countStat][countSide]) # Add the player's sided stat into the temp list
            tempLst.append(playersLst[countPlayer][1]) # Add the player's team initial into the end of the temp list
            if playersLst[countPlayer][1] not in matchTeamsLst: # If the team name is not in the match's teams list,
                matchTeamsLst.append(playersLst[countPlayer][1]) # Add the team's initial into the match's teams list
            statSidedLst.append(tempLst) # Add the temporary list into the stat list with sides

    detect_diff_map(matchTeamsLst, mapLst, statSidedLst)

    matchScores = [get_match_scores(matchScoresRaw)[i:i+2] for i in range(0, len(get_match_scores(matchScoresRaw)), 2)]
    mapLst_noAll = mapLst.copy()
    mapLst_noAll.remove("All Maps")
    teamMatchResDict = {i:0 for i in matchTeamsLst}
    # print(teamMatchResDict)
    matchResStr = f"{matchTeamsLst[0]} vs. {matchTeamsLst[1]}, "
    mapTeamWinLst = []
    team1RoundTotal = 0
    team2RoundTotal = 0
    for countScore in range(len(matchScores)):
        matchResStr += f"{mapLst_noAll[countScore]} {matchScores[countScore][0]}:{matchScores[countScore][1]}"
        team1RoundTotal += matchScores[countScore][0]
        team2RoundTotal += matchScores[countScore][1]
        matchResStr += ", "
        teamMatchResDict[matchTeamsLst[matchScores[countScore].index(max(matchScores[countScore]))]] += 1
        mapTeamWinLst.append(matchTeamsLst[matchScores[countScore].index(max(matchScores[countScore]))])
    matchWinRes = max(teamMatchResDict, key=teamMatchResDict.get)
    matchResStr += f"{matchWinRes} wins"
    # matchWinLst = [[mapTeam, max(teamMatchResDict, key=teamMatchResDict.get)] for mapTeam in mapTeamWinLst]
    matchWinLst = mapTeamWinLst.copy()
    matchWinLst.insert(1, matchWinRes)
    # matchWinLst = [i for i in mapTeamWinLst]
    matchTeamWinLst = [[mapLst[count], matchWinLst[count]] for count in range(len(mapLst))][::-1]
    print(matchResStr)
    print(matchWinLst, mapLst, matchTeamWinLst)

    for countStat in range(len(statSidedLst)):
        statSidedLst[countStat].append(teamNameLst[matchTeamsLst.index(statSidedLst[countStat][-1])])
        # print(statSidedLst[countStat])
        oppTeam = teamNameLst.copy()
        oppTeam.remove(statSidedLst[countStat][-1])
        statSidedLst[countStat].extend(oppTeam)
        statSidedLst[countStat].extend(matchInfo)
        statSidedLst[countStat].append(urlMatch)
        statSidedLst[countStat].append(matchDateTime)

    for countStatSided in range(len(statSidedLst)):
        # print(statSidedLst[countStatSided])
        statSidedLst_extra.append(statSidedLst[countStatSided])
        time.sleep(0.01)
        print(f"statSidedLst_imp: {len(statSidedLst_imp)}, statSidedLst_extra: {len(statSidedLst_extra)}", end="\r", flush=True)

    for countStatSided_imp in range(len(statSidedLst)):
        tempLst = []
        if statSidedLst[countStatSided_imp][2] != 'All':
            continue
        tempLst.append(statSidedLst[countStatSided_imp][0]) # Name
        tempLst.append(statSidedLst[countStatSided_imp][1]) # Map Name
        tempLst.append(statSidedLst[countStatSided_imp][2]) # Side (All)
        tempLst.append(statSidedLst[countStatSided_imp][4]) # ACS
        tempLst.append(statSidedLst[countStatSided_imp][5]) # Kills
        tempLst.append(statSidedLst[countStatSided_imp][6]) # Deaths
        tempLst.append(statSidedLst[countStatSided_imp][7]) # Assists
        tempLst.append(statSidedLst[countStatSided_imp][8]) # KD
        tempLst.append(statSidedLst[countStatSided_imp][-7]) # Name
        tempLst.append(statSidedLst[countStatSided_imp][-6]) # Name
        tempLst.append(statSidedLst[countStatSided_imp][-5]) # Name
        tempLst.append(statSidedLst[countStatSided_imp][-4]) # Name
        tempLst.append(statSidedLst[countStatSided_imp][-3]) # Name
        tempLst.append(urlMatch) # Datetime
        tempLst.append(matchDateTime)
        # print(tempLst)
        statSidedLst_imp.append(tempLst)
        time.sleep(0.01)
        print(f"statSidedLst_imp: {len(statSidedLst_imp)}, statSidedLst_extra: {len(statSidedLst_extra)}", end="\r", flush=True)


def stat_no_sides(statSidedLst_imp, statSidedLst_extra, matchStatsRaw, matchScoresRaw, statNumLst, statNumLst_raw, statSideInd, playersLst, mapLst, teamNameLst, matchInfo, urlMatch, matchDateTime):
    
    num_stats_imp = 5

    # Adding the stat numbers
    add_stat_nums_into_non_main_lst(matchStatsRaw, statNumLst, statNumLst_raw, statSideInd, num_stats_imp)

    matchTeamsLst = [] # Empty list of teams in the match

    for countPlayer in range(len(playersLst)): # For each player in the match
        playersLst[countPlayer].extend(statNumLst[countPlayer]) # Extend the player's list with the stat numbers list
        playersLst[countPlayer].insert(1, 'All') # Add 'All' as the side of the map being played at
        playersLst[countPlayer].append(playersLst[countPlayer][2]) # Add the player's team initial at the end of the list 
        playersLst[countPlayer].pop(2) # Remove the original player's team initial
        if playersLst[countPlayer][-1] not in matchTeamsLst: # If the team name is not in the match's teams list,
            matchTeamsLst.append(playersLst[countPlayer][-1]) # The team name will be added into the list

    detect_diff_map(matchTeamsLst, mapLst, None, playersLst)

    matchScores = [get_match_scores(matchScoresRaw)[i:i+2] for i in range(0, len(get_match_scores(matchScoresRaw)), 2)]
    mapLst_noAll = mapLst.copy()
    mapLst_noAll.remove("All Maps")
    teamMatchResDict = {i:0 for i in matchTeamsLst}
    # print(teamMatchResDict)
    matchResStr = f"{matchTeamsLst[0]} vs. {matchTeamsLst[1]}, "
    mapTeamWinLst = []
    teamsRoundTotal = [0, 0]
    teamsMapRoundsTotal = [0 for i in mapLst_noAll]
    for countScore in range(len(matchScores)):
        matchResStr += f"{mapLst_noAll[countScore]} {matchScores[countScore][0]}:{matchScores[countScore][1]}"
        teamsRoundTotal[0] += matchScores[countScore][0]
        teamsRoundTotal[1] += matchScores[countScore][1]
        matchResStr += ", "
        teamMatchResDict[matchTeamsLst[matchScores[countScore].index(max(matchScores[countScore]))]] += 1
        mapTeamWinLst.append(matchTeamsLst[matchScores[countScore].index(max(matchScores[countScore]))])
    matchWinRes = max(teamMatchResDict, key=teamMatchResDict.get)
    matchLossRes = min(teamMatchResDict, key=teamMatchResDict.get)
    matchResStr += f"{matchWinRes} wins"
    # matchWinLst = [[mapTeam, max(teamMatchResDict, key=teamMatchResDict.get)] for mapTeam in mapTeamWinLst]
    matchWinLst = mapTeamWinLst.copy()
    matchWinLst.insert(1, matchWinRes)
    # matchWinLst = [i for i in mapTeamWinLst]
    matchTeamWinLst = [[mapLst[count], matchWinLst[count]] for count in range(len(mapLst))]
    print(matchResStr)
    print(matchWinLst, mapLst, matchTeamWinLst)
    print(teamsRoundTotal[matchTeamsLst.index(matchWinRes)] - teamsRoundTotal[matchTeamsLst.index(matchLossRes)])
        
    for countPlayerStat in range(len(playersLst)):
        playersLst[countPlayerStat].append(teamNameLst[matchTeamsLst.index(playersLst[countPlayerStat][-1])])
        print(playersLst[countPlayerStat])
        for countMatchWin in matchTeamWinLst:
            if playersLst[countPlayerStat][1] == countMatchWin[0] and playersLst[countPlayerStat][-2] == countMatchWin[1]:
                if countMatchWin[0] == "All Maps":
                    print(f"Match win {teamMatchResDict[countMatchWin[1]]}")
                else:
                    print(f"Map win {teamMatchResDict[countMatchWin[1]]}")
                break
            else:
                if countMatchWin[0] == "All Maps":
                    print(f"Match lost {teamMatchResDict[countMatchWin[1]]}")
                else:
                    print(f"Map lost {teamMatchResDict[countMatchWin[1]]}")
                break
        oppTeam = teamNameLst.copy()
        oppTeam.remove(playersLst[countPlayerStat][-1])
        playersLst[countPlayerStat].extend(oppTeam)
        playersLst[countPlayerStat].extend(matchInfo)
        playersLst[countPlayerStat].append(urlMatch)
        playersLst[countPlayerStat].append(matchDateTime)
        statSidedLst_imp.append(playersLst[countPlayerStat])
        time.sleep(0.01)
        print(f"statSidedLst_imp: {len(statSidedLst_imp)}, statSidedLst_extra: {len(statSidedLst_extra)}", end="\r", flush=True)

def stats_match_new(statSidedLst_imp, statSidedLst_extra, matchStatsRaw, matchScoresRaw, playersLst, mapLst, teamNameLst, matchInfo, urlMatch, matchDateTime):
    statSideInd = matchStatsRaw[0].text.split()
    statNumLst = [] # Empty list of stat numbers
    statNumLst_raw = [] # Empty list of stat numbers in raw form (list in a list, each element has 3 sides)

    if len(statSideInd) != 0: # if the stat has all 3 sides,

        stat_with_sides(statSidedLst_imp, statSidedLst_extra, matchStatsRaw, matchScoresRaw, statNumLst, statNumLst_raw, statSideInd, playersLst, mapLst, teamNameLst, matchInfo, urlMatch, matchDateTime)
    
    else: # If the stat has only one side ('All'),

        stat_no_sides(statSidedLst_imp, statSidedLst_extra, matchStatsRaw, matchScoresRaw, statNumLst, statNumLst_raw, statSideInd, playersLst, mapLst, teamNameLst, matchInfo, urlMatch, matchDateTime)