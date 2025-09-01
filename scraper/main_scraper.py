import requests
from bs4 import BeautifulSoup
import urllib.request as urllib2
from time import strptime
import re
import csv
import calendar
from datetime import datetime
from comm_scraper import beautifulSoupWebScrapeVLRComments
from match_scraper import VCTScraper

# # URL
# url_base = "https://www.vlr.gg/search/threads/?q=" # URL base
# playerNames = ['f0rsaken', 'jinggg', 'd4v41', 'mindfreak', 'something', 'benkai', 'patmen']
# # playerNames = ['f0rsaken']

# # for loop parts
# loopCount_list = []
# for i in range(len(playerNames)):
#     url_example = url_base + playerNames[i]
#     aPage_raw = BeautifulSoup(requests.get(url_example).content, 'html.parser').find_all("a", class_="btn mod-page") # Find all <div> tags that contains posts' texts
#     numPage = []
#     for tag in aPage_raw:
#         numPage.append(int(tag.text))
#     loopCount_list.append(numPage[-1])

# print(loopCount_list)

# # Lists
# titleThread_finalLst = []
# for i in range(len(playerNames)):
#     titleThread_finalLst.append(list())
    
# threadType_finalLst = []
# for i in range(len(playerNames)):
#     threadType_finalLst.append(list())
    
# comm_finalLst = []
# for i in range(len(playerNames)):
#     comm_finalLst.append(list())
    
# flagComm_finalLst = []
# for i in range(len(playerNames)):
#     flagComm_finalLst.append(list())
    
# voteComm_finalLst = []
# for i in range(len(playerNames)):
#     voteComm_finalLst.append(list())
    
# dateComm_finalLst = []
# for i in range(len(playerNames)):
#     dateComm_finalLst.append(list())
    
# timeComm_finalLst = []
# for i in range(len(playerNames)):
#     timeComm_finalLst.append(list())
    
# dateThread_finalLst = []
# for i in range(len(playerNames)):
#     dateThread_finalLst.append(list())
    
# timeThread_finalLst = []
# for i in range(len(playerNames)):
#     timeThread_finalLst.append(list())
    
# print(titleThread_finalLst)
# print(threadType_finalLst)
# print(comm_finalLst)
# print(flagComm_finalLst)
# print(voteComm_finalLst)
# print(dateComm_finalLst)
# print(timeComm_finalLst)
# print(dateThread_finalLst)
# print(timeThread_finalLst)

# for i in range(len(playerNames)):
#     beautifulSoupWebScrapeVLRComments(url_base, 
#                               playerNames[i], 
#                               loopCount_list[i], 
#                               titleThread_finalLst[i], 
#                               threadType_finalLst[i], 
#                               comm_finalLst[i],  
#                               flagComm_finalLst[i],
#                               voteComm_finalLst[i], 
#                               dateComm_finalLst[i], 
#                               timeComm_finalLst[i], 
#                               dateThread_finalLst[i], 
#                               timeThread_finalLst[i])

vct2025_link = "https://www.vlr.gg/vct-2025"
vct2025_year = "2025"
vct2025_upcomingEvents = [
    "Valorant Champions 2025"
]

statSidedLst_imp_vct2025, statSidedLst_extra_vct2025 = VCTScraper(vct2025_link, vct2025_year, vct2025_upcomingEvents)

print(statSidedLst_imp_vct2025)
print(statSidedLst_extra_vct2025)