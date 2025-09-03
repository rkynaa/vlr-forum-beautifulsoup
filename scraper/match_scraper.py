import requests
from bs4 import BeautifulSoup
import urllib.request as urllib2
from time import strptime
import re
import csv
import calendar
from datetime import datetime
from utils.match_utils import datetime_match, info_match, maps_match, players_match, stats_match_new
from utils.event_utils import detect_completed_events
import time, random

# VCTScrapper Function:
# Args:
#  - vctLink (Link of VCT of a specific year)
#  - year (year of the VCT)
#  - upcomingEvent (list of upcoming events)
#   -> Default value = No upcoming events
def VCTScraper(vctLink, year, upcomingEvent=[]):
    vctSoup = BeautifulSoup(requests.get(vctLink).content, 'html.parser')
    
    queryCompletedMatches = vctSoup.find_all("a", class_="wf-card mod-flex event-item") # Query Results for finding events

    urlBase = "https://www.vlr.gg"
    
    urlEventsLst, eventTitlesLst = detect_completed_events(urlBase, upcomingEvent, queryCompletedMatches) # List of URLs and titles for Events
    
    urlEventsLst = urlEventsLst[::-1] # Reversing the order from latest to earliest events for the events' URLs
    eventTitlesLst = eventTitlesLst[::-1] # Reversing the order from latest to earliest events for the events' titles

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
            queryMatchScore = soupMatch.find_all("div", class_="score")
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
            
            # print(queryMatchScore)
            
            # Match's map list
            mapLst = maps_match(queryMatchMaps, queryMatchMapsDisabled)

            # print(matchDateTimeFinal, urlMatch, mapLst) # Checking if the match's datetime, URL and played maps are correct
            
            # Making the list of players in the match
            playersLst = players_match(queryMatchPlayers)
            # print(f"{teamNameLst} {matchInfo} {mapLst} {len(playersLst)}, {matchDateTimeFinal} {urlMatch}")
            
            print(f"{urlMatch}")
            
            stats_match_new(statSidedLst_imp, statSidedLst_extra, queryMatchStats, queryMatchScore, playersLst, mapLst, teamNameLst, matchInfo, urlMatch, matchDateTimeFinal)

    return statSidedLst_imp, statSidedLst_extra