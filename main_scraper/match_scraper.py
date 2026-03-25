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

    # print(vctLinkUpcommingEvents)

    if len(vctLinkUpcommingEvents) != 0:
        print("\nUpcoming Events...\n")
        for vctLinkEventBlock in vctLinkUpcommingEvents:
            vctLinkEvent = vctLinkEventBlock.get("href")
            # vctLinkEventLst = vctLinkEvent.split('/')
            # vctLinkEventLst.insert(2, 'matches')
            # # print(vctLinkEventLst)
            # vctLinkEvent = '/'.join(vctLinkEventLst) + "/?series_id=all"
            vctLinkEvent = baseUrl + vctLinkEvent

            vctDivEventTitle = vctLinkEventBlock.find("div", {"class":"event-item-title"})
            vctEventTitle = vctDivEventTitle.text.strip()

            vctDivPrizePool = vctLinkEventBlock.find("div", {"class":"mod-prize"})
            vctPrizePool = vctDivPrizePool.text.strip().split()[0]
            print(vctEventTitle, vctPrizePool, vctLinkEvent)
    
    if len(vctLinkCompletedEvents) != 0:
        print("\nCompleted Events...\n")
        for vctLinkEventBlock in vctLinkCompletedEvents:
            vctLinkEvent = vctLinkEventBlock.get("href")
            vctLinkEventLst = vctLinkEvent.split('/')
            vctLinkEventLst.insert(2, 'matches')
            # print(vctLinkEventLst)
            vctLinkEvent = '/'.join(vctLinkEventLst) + "/?series_id=all"
            vctLinkEvent = baseUrl + vctLinkEvent

            vctDivEventTitle = vctLinkEventBlock.find("div", {"class":"event-item-title"})
            vctEventTitle = vctDivEventTitle.text.strip()

            vctDivPrizePool = vctLinkEventBlock.find("div", {"class":"mod-prize"})
            vctPrizePool = vctDivPrizePool.text.strip().split()[0]
            print(vctEventTitle, vctPrizePool, vctLinkEvent)
    # print(vctLinkCompletedEvents)
    # print(vctDivEventCols)
    time.sleep(5)
    return None

def match_scraper():
    return None