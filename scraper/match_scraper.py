import requests
from bs4 import BeautifulSoup
import urllib.request as urllib2
from time import strptime
import re
import csv
import calendar
from datetime import datetime
from utils.match_utils import datetime_match, info_match, maps_match, players_match
import time, random

# VCTScrapper Function:
# Args:
#  - vctLink (Link of VCT of a specific year)
#  - year (year of the VCT)
#  - upcomingEvent (list of upcoming events)
#   -> Default value = No upcoming events
def VCTScraper(vctLink, year, upcomingEvent=[]):
    vctSoup = BeautifulSoup(requests.get(vctLink).content, 'html.parser')
    
    urlEventsLst = [] # List of URLs for Events
    eventTitlesLst = [] # List of events' titles
    
    queryCompletedMatches = vctSoup.find_all("a", class_="wf-card mod-flex event-item") # Query Results for finding events

    urlBase = "https://www.vlr.gg"
    
    for resultCompletedMatch in queryCompletedMatches: # For each query result
        url_event = urlBase + resultCompletedMatch.get('href') # Link to each event
        soupEvent = BeautifulSoup(requests.get(url_event).content, 'html.parser') # Soup for specific event
        titleEvent = soupEvent.find_all("title") # Web Title of the Event's VLR webpage
        webTitleLst = " ".join(titleEvent[0].text.split()).split("|")[0].split(":") # Event Web Title Broken down into a list
        
        # Getting the event's title
        eventTitle = "" # Initialize Event Title's name
        if len(webTitleLst) == 2: # If the event web title has only one ":" symbol,
            eventTitle += webTitleLst[0] # The first element is the event's title
            
        else: # If the event web title has two ":" symbols (i.e., 'VCT 2025: China Stage 2: Brackets, Groups, and Standings '),
            eventTitle += webTitleLst[0] + ":" + webTitleLst[1] # the first two elements are the event's title
        
        
        # Web Scraping for completed events only
        if eventTitle in upcomingEvent: # If the event is not completed,
            continue # It will be skipped
        
        else: # If the event is already completed,
            eventLinks = soupEvent.find_all("a", class_="wf-nav-item") # Query results for event link
            eventPartLink = eventLinks[1].get('href') # Getting the partial link of the event
            eventPartLink = eventPartLink.split("?")[0] + "?" + "series_id=all" # Getting the partial link of the event's overall matches
            matchesEventLink = urlBase + eventPartLink # Completing the event's link
            
            eventTitlesLst.append(eventTitle) # Adding the event's title into the events' titles list
            urlEventsLst.append(matchesEventLink) # Adding the event's url into the events' titles list

    urlEventsLst = urlEventsLst[::-1] # Reversing the order from latest to earliest events for the events' URLs
    eventTitlesLst = eventTitlesLst[::-1] # Reversing the order from latest to earliest events for the events' titles
    
    # for count in range(len(urlEventsLst)): # For each events' urls
    #     print(eventTitlesLst[count], urlEventsLst[count]) # Printing the completed events' titles and URLs

    statSidedLst_imp = [] # List of players' stats (with sides, including all sides) that only contains important stats (ACS, K, D, A, KD)
    statSidedLst_extra = [] # List of players' stats (with sides, including all sides) that contains overall stats (Warning: might have missing values)
    
    # for urlEvent in urlEventsLst: # for each events' URLs
    for count in range(len(urlEventsLst)): # For each events' urls
        print(f"{eventTitlesLst[count]}, {urlEventsLst[count]}\n") # Printing the completed events' titles and URLs
        urlMatches = urlEventsLst[count] # the URL of the event's all matches, including the showmatch
        soupMatches = BeautifulSoup(requests.get(urlMatches).content, 'html.parser') # Soup of the event's matches
        queryMatches = soupMatches.find_all("a", {'class':['wf-module-item', 'match-item', 'mod-color']}) # Query results for all matches

        for resultMatches in queryMatches: # For each query result for all matches
            urlMatch = urlBase + resultMatches.get('href') # Complete URL link for the match

            soupMatch = BeautifulSoup(requests.get(urlMatch).content, 'html.parser') # Soup for the match
            
    #         # print(urlMatch) # Checking if the URL is correct
            
            # Queries
            queryMatchPlayers = soupMatch.find_all("td", class_="mod-player") # Query results for players in the match
            queryMatchStats = soupMatch.find_all("td", class_="mod-stat") # Query results for players' stats in the match
            queryMatchMaps = soupMatch.find_all('div', class_='js-map-switch') # Query results for maps in the match
            queryMatchMapsDisabled = soupMatch.find_all('div', class_="mod-disabled") # Query results for unplayed maps in the match
            # matchTitle = soupMatch.find_all("title") # Query results for match title in the match
            queryMatchDatetime = soupMatch.find_all("div", class_="moment-tz-convert") # Query results for datetime in the match       
            queryMatchTitle = soupMatch.find_all('title') # Query results for the match's title
            matchTitleLst = queryMatchTitle[0].text.strip().split(' | ')
            matchTitle = " ".join(matchTitleLst).lower()

            if "showmatch" in matchTitle: # If showmatch is the current match,
                # print("Showmatch Detected!\n")
                continue # It won't be added

            # Match's datetime
            matchDateTimeFinal = datetime_match(year, queryMatchDatetime)

            # print(matchDateTimeNew, urlMatch) # Checking if the remade match's datetime and URl is correct
            
            # Match's extra info
            matchInfo, teamNameLst = info_match(queryMatchTitle)
            
            
            # Match's map list
            # for i in queryMatchMaps:
            #     print(i.text.strip().split())
            mapLst = maps_match(queryMatchMaps, queryMatchMapsDisabled)

            # print(matchDateTimeFinal, urlMatch, mapLst) # Checking if the match's datetime, URL and played maps are correct
            
            # Making the list of players in the match
            playersLst = players_match(queryMatchPlayers)
            print(f"{teamNameLst} {matchInfo} {mapLst} {len(playersLst)}, {matchDateTimeFinal} {urlMatch}")
            
            # statSideInd = len(" ".join(queryMatchStats[1].text.split()).replace("/", "").split()) # Checking if the stats has all 3 sides
            # statSideInd = "." in " ".join(queryMatchStats[1].text.split()).replace("/", "").split()[0]
            statSideInd = queryMatchStats[0].text.split()
            
            # print("." in " ".join(queryMatchStats[1].text.split()).replace("/", "").split()[0])
            # print(statSideInd, " ".join(queryMatchStats[1].text.split()).replace("/", "").split()[0])
            
            statNumLst = [] # Empty list of stat numbers
            noneText = "".join(queryMatchStats[0].text.split()) # Example of empty text
            statNumLst_raw = [] # Empty list of stat numbers in raw form (list in a list, each element has 3 sides)

            # print(statSideInd)
            
            if len(statSideInd) != 0: # if the stat has all 3 sides,
                
                # Adding the stat numbers
                for queryMatchStat in queryMatchStats: # for each query result of the match stat
                    textTag = " ".join(queryMatchStat.text.split()).replace("/", "").split(" ") # Removing the '/' part of the stat, to get the necessary part
                    if textTag == noneText: # If the result text tag is empty,
                        continue # Skip the stat
                    else: # If actually contains a stat,
                        if len(textTag) == 5: # If there's a leading and trailing spaces in the text tag,
                            textTag = textTag[1:-1] # Removed the leading and trailing spaces in the text tag
                        statNumLst_raw.append(textTag) # Add the stat into the raw list of stat numbers

                for countStatNum_raw in range(0, len(statNumLst_raw), 12): # For each 12 numbers in the raw list
                    tempLst = [] # Empty temporary stats List
                    for countStat in range(12): # for each stat in the 12 numbers of stats
                        tempLst.append(statNumLst_raw[countStatNum_raw+countStat]) # Add each stats
                    statNumLst.append(tempLst) # Add the temporary stats list into the list of stats numbers 

                for countPlayer in range(len(playersLst)): # For each player in the player list
                    playersLst[countPlayer].extend(statNumLst[countPlayer]) # Each player's list got extended with the stat numbers' list
                    # print(playerLst[countPlayer]) # Checking if the data is correct

                statSidedLst = [] # Empty list of stats with sides

                sides = ['All', 'Atk', 'Def'] # Each sides in a match (including 'All')

                matchTeamsLst = [] # Empty list of teams in the match
                
                # print(playersLst[0])

                for countPlayer in range(len(playersLst)): # For each player in the match
                    for countSide in range(3): # For each side the player played in
                        tempLst = [] # Temporary Empty List to store the proper format of the player stats
                        tempLst.append(playersLst[countPlayer][0]) # Add the player's name into the temp list
                        tempLst.append(sides[countSide]) # Add the side of the player played in into the temp list
                        for countStat in range(2, len(playersLst[0]), 1): # For each stat in the player's list, EXCEPT the player's name and team name
                            # print(playerLst[k][m], l)
                            # if len(playerLst[i][k]) < 3:
                            #     while len(playerLst[i][k]) != 3:
                            #         playerLst[i][k].append('-')
                            # tempLst.append(playerLst[k][m][l])
                            
                            # print(playerLst[k][m], j, len(playerLst[k][m]) != 3)
                            if len(playersLst[countPlayer][countStat]) < 3: # If the stat is INCOMPLETE (missing stat numbers),
                                while len(playersLst[countPlayer][countStat]) != 3: # While the stat is not complete yet,
                                    playersLst[countPlayer][countStat].append('-') # Fill the empty part of the list with '-' to be easily filtered
                            tempLst.append(playersLst[countPlayer][countStat][countSide]) # Add the player's sided stat into the temp list
                            
                        tempLst.append(playersLst[countPlayer][1]) # Add the player's team initial into the end of the temp list
                        if playersLst[countPlayer][1] not in matchTeamsLst: # If the team name is not in the match's teams list,
                            matchTeamsLst.append(playersLst[countPlayer][1]) # Add the team's initial into the match's teams list
                        statSidedLst.append(tempLst) # Add the temporary list into the stat list with sides

                # print(matchTeamsLst) # Print the teams that played in the match, checking the value

                teamPlayerLst = {i:0 for i in matchTeamsLst}
                # print(teamPlayerLst)

                countMapPlayed = 0
                for countStat in range(len(statSidedLst)):
                    playerTeam = statSidedLst[countStat][-1]
                    playerName = statSidedLst[countStat][0]
                    if playerTeam != statSidedLst[countStat-1][-1] and teamPlayerLst[statSidedLst[countStat-1][-1]] != 0 and teamPlayerLst[playerTeam] != 0 and countStat != 0 and countStat != len(statSidedLst):
                        # print("New Map!")
                        countMapPlayed += 1
                        teamPlayerLst[playerTeam] = 0
                        teamPlayerLst[statSidedLst[countStat-1][-1]] = 0
                    teamPlayerLst[playerTeam] += 1
                    statSidedLst[countStat].insert(1, mapLst[countMapPlayed])
                    if '+' in statSidedLst[countStat][8]:
                        statSidedLst[countStat][8] = statSidedLst[countStat][8][1]
                    if '+' in statSidedLst[countStat][-2]:
                        statSidedLst[countStat][-2] = statSidedLst[countStat][-2][1]

                for countStat in range(len(statSidedLst)):
                    statSidedLst[countStat].append(teamNameLst[matchTeamsLst.index(statSidedLst[countStat][-1])])
                    oppTeam = teamNameLst.copy()
                    oppTeam.remove(statSidedLst[countStat][-1])
                    statSidedLst[countStat].extend(oppTeam)
                    statSidedLst[countStat].extend(matchInfo)
                    statSidedLst[countStat].append(urlMatch)
                    statSidedLst[countStat].append(matchDateTimeFinal)
                
                # print(teamPlayerLst) # Print the teams that played in the match, checking the value

                for countStatSided in range(len(statSidedLst)):
                    # print(statSidedLst[countStatSided])
                    statSidedLst_extra.append(statSidedLst[countStatSided])
                    # print("statSidedLst_extra: ", len(statSidedLst_extra))
                    time.sleep(0.01)
                    print(f"statSidedLst_extra: {len(statSidedLst_extra)}", end="\r", flush=True)
                print()

                # statSidedLstImp = []
                print(statSidedLst)
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
                    tempLst.append(matchDateTimeFinal)
                    # print(tempLst)
                    # statSidedLstImp.append(tempLst)
                    statSidedLst_imp.append(tempLst)
                    time.sleep(0.01)
                    print(f"statSidedLst_imp: {len(statSidedLst_imp)}", end="\r", flush=True)
            
            else: # If the stat has only one side ('All'),
                
                # Adding the stat numbers
                for queryMatchStat in queryMatchStats: # for each query result of the match stat
                    textTag = "".join(queryMatchStat.text.split()).replace("/", "") # Removing the '/' part of the stat, to get the necessary part
                    if textTag == noneText: # If the result text tag is empty,
                        continue # Skip the stat
                    else: # If actually contains a stat,
                        statNumLst_raw.append(textTag) # Add the stat into the raw list of stat numbers

                for countStatNum_raw in range(0, len(statNumLst_raw), 5): # For each 5 numbers in the raw list
                    tempLst = [] # Empty temporary stats List
                    for countStat in range(5): # for each stat in the 5 numbers of stats
                        tempLst.append(statNumLst_raw[countStatNum_raw+countStat]) # Add each stats
                    statNumLst.append(tempLst) # Add the temporary stats list into the list of stats numbers

                matchTeamsLst = [] # Empty list of teams in the match

                for countPlayer in range(len(playersLst)): # For each player in the match
                    playersLst[countPlayer].extend(statNumLst[countPlayer]) # Extend the player's list with the stat numbers list
                    playersLst[countPlayer].insert(1, 'All') # Add 'All' as the side of the map being played at
                    # print(playersLst[countPlayer][2])
                    playersLst[countPlayer].append(playersLst[countPlayer][2]) # Add the player's team initial at the end of the list 
                    playersLst[countPlayer].pop(2) # Remove the original player's team initial
                    if playersLst[countPlayer][-1] not in matchTeamsLst: # If the team name is not in the match's teams list,
                        matchTeamsLst.append(playersLst[countPlayer][-1]) # The team name will be added into the list

                # print(matchTeamsLst) # Print the teams that played in the match, checking the value
                
                teamPlayerLst = {i:0 for i in matchTeamsLst}
                # print(teamPlayerLst)

                countMapPlayed = 0
                for countPlayerStat in range(len(playersLst)):
                    playerTeam = playersLst[countPlayerStat][-1]
                    playerName = playersLst[countPlayerStat][0]
                    if playerTeam != playersLst[countPlayerStat-1][-1] and teamPlayerLst[playersLst[countPlayerStat-1][-1]] != 0 and teamPlayerLst[playerTeam] != 0 and countPlayerStat != 0 and countPlayerStat != len(playersLst):
                        # print("New Map!")
                        countMapPlayed += 1
                        teamPlayerLst[playerTeam] = 0
                        teamPlayerLst[playersLst[countPlayerStat-1][-1]] = 0
                    teamPlayerLst[playerTeam] += 1
                    playersLst[countPlayerStat].insert(1, mapLst[countMapPlayed])
                    if '+' in playersLst[countPlayerStat][-2]:
                        playersLst[countPlayerStat][-2] = playersLst[countPlayerStat][-2][1]
                
                # print(teamPlayerLst) # Print the teams that played in the match, checking the value
                    
                for countPlayerStat in range(len(playersLst)):
                    playersLst[countPlayerStat].append(teamNameLst[matchTeamsLst.index(playersLst[countPlayerStat][-1])])
                    oppTeam = teamNameLst.copy()
                    oppTeam.remove(playersLst[countPlayerStat][-1])
                    playersLst[countPlayerStat].extend(oppTeam)
                    playersLst[countPlayerStat].extend(matchInfo)
                    playersLst[countPlayerStat].append(urlMatch)
                    playersLst[countPlayerStat].append(matchDateTimeFinal)
                    # print(playersLst[countPlayerStat])
                    statSidedLst_imp.append(playersLst[countPlayerStat])
                    time.sleep(0.01)
                    print(f"statSidedLst_imp: {len(statSidedLst_imp)}", end="\r", flush=True)
    return statSidedLst_imp, statSidedLst_extra