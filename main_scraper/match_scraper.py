import requests
from bs4 import BeautifulSoup
import urllib.request as urllib2
from time import strptime
import re
import csv
import calendar
from datetime import datetime
# from utils.match_utils import datetime_match, info_match, maps_match, players_match, stats_match_new
# from utils.event_utils import detect_completed_events
import time, random

def vct_scraper(vctYearURL):
    vctYear = vctYearURL.split('-')[1]
    baseUrl = vctYearURL.split('-')[0][:-4]
    # print(baseUrl)

    print(f"Scraping {vctYearURL} for VCT {vctYear}")

    vctYearSoup = BeautifulSoup(requests.get(vctYearURL).content, 'html.parser')
    vctDivEventCols = vctYearSoup.find_all("div", {"class":"events-container-col"})
    vctLinkUpcommingEvents = vctDivEventCols[0].find_all("a", {"class":"wf-card mod-flex event-item"})
    vctLinkCompletedEvents = vctDivEventCols[1].find_all("a", {"class":"wf-card mod-flex event-item"})
    
    vctUpcomingEventTitles = [vctLinkEventBlock.find("div", {"class":"event-item-title"}).text.strip() for vctLinkEventBlock in vctLinkUpcommingEvents]
    vctCompletedEventTitles = [vctLinkEventBlock.find("div", {"class":"event-item-title"}).text.strip() for vctLinkEventBlock in vctLinkCompletedEvents]
    
    vctLinkEventBlocks = vctYearSoup.find_all("a", {"class":"wf-card mod-flex event-item"})
    
    for vctLinkEventBlock in vctLinkEventBlocks:
        vctEventTitle = vctLinkEventBlock.find("div", {"class":"event-item-title"}).text.strip()
        vctPrizePool = vctLinkEventBlock.find("div", {"class":"mod-prize"}).text.strip().split()[0]
        vctLinkEvent = ""
        if vctEventTitle in vctUpcomingEventTitles:
            vctLinkEvent += baseUrl + vctLinkEventBlock.get("href")
            
        elif vctEventTitle in vctCompletedEventTitles:
            vctLinktemp = vctLinkEventBlock.get("href")
            vctLinkEventLst = vctLinktemp.split('/')
            vctLinkEventLst.insert(2, 'matches')
            vctLinkEvent += baseUrl + '/'.join(vctLinkEventLst) + "/?series_id=all"
            
            match_scraper(baseUrl, vctEventTitle, vctLinkEvent)
        
        # print(vctEventTitle, vctLinkEvent)
            
    time.sleep(5)
    return None

def match_scraper(baseUrl, vctEventTitle, vctEventMatchLink):
    vctMatchesSoup = BeautifulSoup(requests.get(vctEventMatchLink).content, 'html.parser')
    vctLinkMatchBlocks = vctMatchesSoup.find_all("a", {"class":"match-item"})
    print(F"Total match for {vctEventTitle} is {len(vctLinkMatchBlocks)}")
    for vctLinkMatchBlock in vctLinkMatchBlocks:    
        vctLinkMatch = baseUrl + vctLinkMatchBlock.get("href")
        vctMatchSoup = BeautifulSoup(requests.get(vctLinkMatch).content, 'html.parser')
        
        matchScore = "".join(vctMatchSoup.find("div", {"class":"match-header-vs-score"}).text.strip().split()[1:4])
        
        matchTeamsLinkLst = vctMatchSoup.find_all("a", {"class":"match-header-link"})
        matchTeamNames = [matchTeamsLink.text.strip() for matchTeamsLink in matchTeamsLinkLst]
        # print(matchTeamNames)
        
        matchStatsAllMaps = vctMatchSoup.find("div", {"class":"vm-stats-game mod-active"})
        matchAllMapsPlayersLst = [" ".join(matchStatsAllMapsPlayer.text.split()[::-1]) for matchStatsAllMapsPlayer in matchStatsAllMaps.find_all("td", {"class":"mod-player"})]
        print(matchAllMapsPlayersLst)
        print(f"{vctEventTitle} ({matchTeamNames[0]} {matchScore} {matchTeamNames[1]}) {vctLinkMatch}")
    return None