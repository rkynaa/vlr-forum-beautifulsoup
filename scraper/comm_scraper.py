import requests
from bs4 import BeautifulSoup
import urllib.request as urllib2
from time import strptime
import re
import csv
import calendar
from datetime import datetime

def beautifulSoupWebScrapeVLRComments(urlBase, 
                                      plyrName, 
                                      loopCount, 
                                      threadTitleLst_plyr, 
                                      threadTypeLst_plyr,  
                                      commLst_plyr,  
                                      commFlagLst_plyr,
                                      commVoteLst_plyr,
                                      commDateLst_plyr,
                                      commTimeLst_plyr,  
                                      threadDateLst_plyr, 
                                      threadPostLst_plyr):
    print("Collecting comments for: " + plyrName + "\n")
    for i in range(loopCount):
        url_extra = "&page="
        url_final = urlBase + plyrName
        if i != 0:
            url_final += url_extra + str(i+1)
        
        print(url_final)
        
        soupRes = BeautifulSoup(requests.get(url_final).content, 'html.parser')
    
        aType_raw = soupRes.find_all("a") # Find all <div> tags that contains posts' texts
        typeDisc = []
        for tag in aType_raw:
            printText = " ".join(tag.text.split())
            if printText == "General Discussion" or printText == "Off Topic" or printText == "Matches" or printText == "News":
                typeDisc.append(printText)
        typeDisc.pop(0)

        aTitle_raw = soupRes.find_all("a", class_="thread-item-header-title") # Find all <div> tags that contains posts' texts
        spanDate_raw = soupRes.find_all("span", class_="date-full hide")
        
        titleLst = []
        for tag in aTitle_raw:
            titleLst.append(" ".join(tag.text.split()))
        
        dateLst = []
        for tag in spanDate_raw:
            datetimeVLRPost = [a.strip().replace(',', '') for a in " ".join(tag.text.split()).split("at")]
            month = list(calendar.month_name).index(datetimeVLRPost[0].split(" ")[0])
            date = datetimeVLRPost[0].split(" ")[1]
            year = datetimeVLRPost[0].split(" ")[-1]
            datePost = date+"/"+str(month)+"/"+year
            dateLst.append(datePost)

        timeLst = []
        for tag in spanDate_raw:
            datetimeVLRPost = [a.strip().replace(',', '') for a in " ".join(tag.text.split()).split("at")]
            hour = int(datetimeVLRPost[1].split(" ")[0].split(":")[0])
            minute = datetimeVLRPost[1].split(" ")[0].split(":")[1]
            if datetimeVLRPost[1].split(" ")[1] == "PM" and hour != 12:
                hour += 12
            timePost = str(hour)+":"+minute
            timeLst.append(timePost)

        typeDiscWithVotes = []
        titleLstWithVotes = []
        dateLstWithVotes = []
        timeLstWithVotes = []

        for j in range(len(typeDisc)):
            if typeDisc[j] == "Matches" or typeDisc[j] == "News":
                continue
            else:
                typeDiscWithVotes.append(typeDisc[j])
                titleLstWithVotes.append(titleLst[j])
                dateLstWithVotes.append(dateLst[j])
                timeLstWithVotes.append(timeLst[j])

        commThreads_lst = []
        commVoteThread_lst = []
        dateCommThreadLst = []
        timeCommThreadLst = []
        flagCommThreadLst = []

        print("\nAnalyzing thread comments...")
        for tags in aTitle_raw:
            threadLink = "https://www.vlr.gg" + tags.get('href')
            soupThread = BeautifulSoup(requests.get(threadLink).content, 'html.parser')
            soupDetectMatch = soupThread.find_all('a', class_="match-header-event")
            soupDetectNews = soupThread.find_all('a', class_='article-meta-author')
            if len(soupDetectMatch) == 1 or len(soupDetectNews) == 1:
                print(threadLink + " will not be added")
                continue

            commTemp_lst = []
            voteTemp_lst = []
            dateTemp_lst = []
            timeTemp_lst = []
            flagTemp_lst = []
            
            soupEdit = soupThread.find_all('span', class_="post-edit")
            for edit in soupEdit:
                edit.span.decompose()
                
            spanCommDate_raw = soupThread.find_all('span', class_="js-date-toggle")
            for tag in spanCommDate_raw:
                dateComm = tag.get('title').split("at")[0].strip().replace(",", "")
                month = list(calendar.month_abbr).index(dateComm.split(" ")[0])
                date = dateComm.split(" ")[1]
                year = dateComm.split(" ")[-1]
                datePost = date+"/"+str(month)+"/"+year

                # timeComm = k.split("at")[1].strip()
                timeComm = tag.get('title').split("at")[1].strip()
                hour = int(timeComm.split(" ")[0].split(":")[0])
                minute = timeComm.split(" ")[0].split(":")[1]
                if timeComm.split(" ")[1] == "PM" and hour != 12:
                    hour += 12
                timePost = str(hour)+":"+minute
                
                dateTemp_lst.append(datePost)
                timeTemp_lst.append(timePost)
            
            commThreads_raw = soupThread.find_all('div', class_='post-body')
#             commThreads_raw
            for tag in commThreads_raw:
                commTemp_lst.append(deEmojify(re.sub(r'http\S+', '', " ".join(tag.text.split())).strip()))
#             print(len(commThreads_lst))

            flagCommThread_raw = soupThread.find_all('i', class_="post-header-flag")
            for tag in flagCommThread_raw:
                flagTemp_lst.append(tag.get("title"))
            
            commVoteThread_raw = soupThread.find_all('div', class_='post-frag-count')
#             commVoteThread_raw
            for tag in commVoteThread_raw:
                voteTemp_lst.append(" ".join(tag.text.split()))
#             print(len(commVoteThread_lst))
            
            commThreadHeadVote_raw = soupThread.find_all('div', id="thread-frag-count")
            commThreadHeadVote = list()
            for tag in commThreadHeadVote_raw:
                commThreadHeadVote.append(int(" ".join(tag.text.split())))
#           print(commThreadHeadVote[0])

            voteTemp_lst.insert(0, commThreadHeadVote[0])
            # print(len(voteTemp_lst))
            
            commThreads_lst.append(commTemp_lst)
            flagCommThreadLst.append(flagTemp_lst)
            commVoteThread_lst.append(voteTemp_lst)
            dateCommThreadLst.append(dateTemp_lst)
            timeCommThreadLst.append(timeTemp_lst)
        
        print("Submitting all comments...")

        for j in range(len(typeDiscWithVotes)):
            for k in range(len(commThreads_lst[j])):

                # print(titleLstWithVotes[j])
                threadTitleLst_plyr.append(titleLstWithVotes[j])

                # print(typeDiscWithVotes[j])
                threadTypeLst_plyr.append(typeDiscWithVotes[j])

                # print(commThreads_lst[j][k])
                commLst_plyr.append(commThreads_lst[j][k])

                # print(flagCommThreadLst[j][k])
                commFlagLst_plyr.append(flagCommThreadLst[j][k])

                # print(commVoteThread_lst[j][k])
                commVoteLst_plyr.append(commVoteThread_lst[j][k])

                # print(dateCommThreadLst[j][k])
                commDateLst_plyr.append(dateCommThreadLst[j][k])

                # print(timeCommThreadLst[j][k])
                commTimeLst_plyr.append(timeCommThreadLst[j][k])

                # print(dateLstWithVotes[j])
                threadDateLst_plyr.append(dateLstWithVotes[j])

                # print(timeLstWithVotes[j])
                threadPostLst_plyr.append(timeLstWithVotes[j])

        print("\n")
    print("Collecting comments for " + plyrName + " is completed\n")