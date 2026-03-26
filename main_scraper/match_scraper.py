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

        matchTeamsProps = [[], []]
        
        matchScore = "".join(vctMatchSoup.find("div", {"class":"match-header-vs-score"}).text.strip().split()[1:4])
        matchBestOfType = vctMatchSoup.find("div", {"class":"match-header-vs-score"}).text.strip().split()[-1]
        # print(matchType)
        matchScoreLst = matchScore.split(':')
        matchScoreIntLst = [int(matchScoreStr) for matchScoreStr in matchScoreLst]
        matchScoreTotal = sum(matchScoreIntLst)
        
        matchTeamsLinkLst = vctMatchSoup.find_all("a", {"class":"match-header-link"})
        matchTeamNames = [matchTeamsLink.text.strip() for matchTeamsLink in matchTeamsLinkLst]
        # print(matchTeamNames)
        
        matchStatsAllMaps = vctMatchSoup.find("div", {"class":"vm-stats-game mod-active"})
        matchAllMapsPlayersLst = [" ".join(matchStatsAllMapsPlayer.text.split()[::-1]) for matchStatsAllMapsPlayer in matchStatsAllMaps.find_all("td", {"class":"mod-player"})]
        matchTeamAggrNames = [matchAllMapsPlayersLst[0].split(' ')[0], matchAllMapsPlayersLst[-1].split(' ')[0]]

        matchDivMapsDecisions = vctMatchSoup.find("div", {"class":"match-header-note"})
        matchMapsDecisionsLst = [matchMapsDecs.strip() for matchMapsDecs in matchDivMapsDecisions.text.strip().split(';')]

        matchMapsPlaysLst = [matchMapsPlays for matchMapsPlays in matchMapsDecisionsLst if "pick" in matchMapsPlays]
        matchMapsPlaysLst.append(matchMapsDecisionsLst[-1])
        matchMapsPlaysTrueLst = [matchMapsPlaysLst[i] for i in range(matchScoreTotal)]

        matchDivGameIDs = vctMatchSoup.find_all("div", {"class":"js-map-switch"})
        matchGameIDs = [matchDivGameID.get("data-game-id") for matchDivGameID in matchDivGameIDs]
        matchGameIDs.remove("all")
        matchGameIDs = matchGameIDs[:matchScoreTotal]
        # print(matchGameIDs)
        matchMapUrls = [vctLinkMatch + "/?game=" + matchGameID + "&tab=overview" for matchGameID in matchGameIDs]

        matchMapScoreStats = map_scraper(matchMapUrls[1])

        print(matchMapScoreStats)

        # for matchMapUrl in matchMapUrls:
        #     # print(matchMapUrl)
        #     map_scraper(matchMapUrl)
        # # print(matchMapUrls)

        for i in range(matchScoreTotal):
            if 'remains' not in matchMapsPlaysTrueLst[i]:
                matchMapsPlaysTrueLst[i] = matchMapsPlaysTrueLst[i].split()[-1]
            else:
                matchMapsPlaysTrueLst[i] = matchMapsPlaysTrueLst[i].split()[0]

        matchDivType = vctMatchSoup.find("div", {"class":"match-header-event-series"})
        matchType = " ".join(matchDivType.text.split())
        # print(matchType, matchMapsPlaysTrueLst, matchScoreTotal)

        # for i in range(len(matchTeamsProps)):
        #     teamName = re.sub(r'\s+',' ',matchTeamNames[i])
        #     if "(" in teamName:
        #         matchTeamsProps[i].append(teamName.split('(')[1][:-1])
        #     else:
        #         matchTeamsProps[i].append(teamName)
        #     matchTeamsProps[i].append(matchTeamAggrNames[i])

        #     matchTeamsProps[i].append(matchScoreLst[i])

        #     if matchMapsDecisionsLst[0].split()[0] == matchTeamAggrNames[i]:
        #         matchTeamsProps[i].append("Team A")
        #     else:
        #         matchTeamsProps[i].append("Team B")

        #     if matchScoreIntLst.index(max(matchScoreIntLst)) == i:
        #         matchTeamsProps[i].append("Match Win")
        #     else:
        #         matchTeamsProps[i].append("Match Loss")

        #     matchTeamsProps[i].append(vctEventTitle)
        #     matchTeamsProps[i].append(matchType)

        #     matchTeamsProps[i].append([playerName for playerName in matchAllMapsPlayersLst if playerName.split()[0] == matchTeamAggrNames[i]])
            
        #     matchTeamMapsDecs = [matchTeamMaps for matchTeamMaps in matchMapsDecisionsLst if matchTeamMaps.split()[0] == matchTeamAggrNames[i]]
        #     matchTeamMapsDecs.append(matchMapsDecisionsLst[-1])
            
        #     matchTeamsProps[i].append(matchTeamMapsDecs)
        #     banLst = []
        #     pickLst = []
        #     for maps in matchTeamMapsDecs:
        #         if 'ban' in maps:
        #             banLst.append(maps.split()[-1])
        #         elif 'pick' in maps:
        #             pickLst.append(maps.split()[-1])
        #         else:
        #             pickLst.append(maps.split()[0])

        #     if len(banLst) != 2:
        #         for j in range(2-len(banLst)):
        #             banLst.append('-')

        #     if len(pickLst) != 3:
        #         for j in range(3-len(pickLst)):
        #             pickLst.append('-')
            
        #     matchTeamsProps[i].append(banLst)
        #     matchTeamsProps[i].append(pickLst)

        #     matchTeamsProps[i].append(matchMapsPlaysTrueLst)

        #     matchTeamsProps[i].append(vctLinkMatch)
            
            # print(matchTeamsProps[i])
        for i in range(len(matchTeamsProps)):
            teamName = re.sub(r'\s+',' ',matchTeamNames[i])
            if "(" in teamName:
                matchTeamsProps[i].append(teamName.split('(')[1][:-1])
            else:
                matchTeamsProps[i].append(teamName)
            matchTeamsProps[i].append(matchTeamAggrNames[i])

            matchTeamsProps[i].append(matchScoreLst[i])

            matchTeamsProps[i].append(matchBestOfType)

            if matchMapsDecisionsLst[0].split()[0] == matchTeamAggrNames[i]:
                matchTeamsProps[i].append("A")
                teamSideIdx = 1
            else:
                matchTeamsProps[i].append("B")
                teamSideIdx = 0

            if matchScoreIntLst.index(max(matchScoreIntLst)) == i:
                matchTeamsProps[i].append("win")
            else:
                matchTeamsProps[i].append("loss")

            # matchTeamMapStats = []
            # matchTeamTotalScore = 0

            # for mapStat in matchMapScoreStats:
            #     mapName = mapStat[0]
            #     mapScore = mapStat[1][teamSideIdx]
            #     tSideScore = mapStat[2][teamSideIdx][0]
            #     ctSideScore = mapStat[2][teamSideIdx][1]

            #     matchTeamMapStats.append([mapName, mapScore, tSideScore, ctSideScore])
            #     matchTeamTotalScore += mapScore

            # matchTeamsProps[i].append(matchTeamMapStats)
            # matchTeamsProps[i].append(matchTeamTotalScore)

            matchTeamMapStats = []
            matchTeamTotalScore = 0
            matchTeamTSideTotal = 0
            matchTeamCTSideTotal = 0

            for mapStat in matchMapScoreStats:
                mapName = mapStat[0]
                mapScore = mapStat[1][teamSideIdx]
                tSideScore = mapStat[2][teamSideIdx][0]
                ctSideScore = mapStat[2][teamSideIdx][1]

                matchTeamMapStats.append([mapName, mapScore, tSideScore, ctSideScore])

                matchTeamTotalScore += mapScore
                matchTeamTSideTotal += tSideScore
                matchTeamCTSideTotal += ctSideScore

            matchTeamsProps[i].append(matchTeamMapStats)
            matchTeamsProps[i].append(matchTeamTotalScore)
            matchTeamsProps[i].append(matchTeamTSideTotal)
            matchTeamsProps[i].append(matchTeamCTSideTotal)

            matchTeamsProps[i].append(vctEventTitle)
            matchTeamsProps[i].append(matchType)

            matchTeamsProps[i].append([playerName for playerName in matchAllMapsPlayersLst if playerName.split()[0] == matchTeamAggrNames[i]])
            
            matchTeamMapsDecs = [matchTeamMaps for matchTeamMaps in matchMapsDecisionsLst if matchTeamMaps.split()[0] == matchTeamAggrNames[i]]
            matchTeamMapsDecs.append(matchMapsDecisionsLst[-1])
            
            # matchTeamsProps[i].append(matchTeamMapsDecs)
            banLst = []
            pickLst = []
            for maps in matchTeamMapsDecs:
                if 'ban' in maps:
                    banLst.append(maps.split()[-1])
                elif 'pick' in maps:
                    pickLst.append(maps.split()[-1])
                else:
                    pickLst.append(maps.split()[0])

            if len(banLst) != 2:
                for j in range(2-len(banLst)):
                    banLst.append('-')

            if len(pickLst) != 3:
                for j in range(3-len(pickLst)):
                    pickLst.append('-')

            if len(matchMapsPlaysTrueLst) != 5:
                for j in range(5-len(matchMapsPlaysTrueLst)):
                    matchMapsPlaysTrueLst.append('-')
            
            matchTeamsProps[i].append(banLst)
            matchTeamsProps[i].append(pickLst)

            matchTeamsProps[i].append(matchMapsPlaysTrueLst)

            matchTeamsProps[i].append(vctLinkMatch)
            
            print(matchTeamsProps[i])

        # print(matchAllMapsPlayersLst, matchMapsDecisionsLst)
        # print(f"{vctEventTitle} ({matchTeamNames[0]} {matchScore} {matchTeamNames[1]}) {vctLinkMatch}")
        colNames = ["team_name", "team_aggr", "pick_team", "match_res", "map_stats", "total_win", "t_win", "ct_win", "event_name", "match_type", "player_list", "ban_map_1", "ban_map_2",
                    "pick_map_1", "pick_map_2", "pick_map_3", "match_map_1", "match_map_2", "match_map_3", "match_map_4", "match_map_5", "match_url"]
        print("\n")
    return None

def map_scraper(vctMapUrl):
    # print(vctMapUrl)
    mapSoup = BeautifulSoup(requests.get(vctMapUrl).content, 'html.parser')
    
    mapDivStatsHeaders = mapSoup.find_all("div", {"class":"vm-stats-game-header"})

    mapStatNames = mapSoup.find_all("div", {"class":"map"})
    mapNames = []
    for mapStatName in mapStatNames:
        mapNames.append(mapStatName.text.strip().split()[0])
    # print(mapNames)

    mapDivScores = mapSoup.find_all("div", {"class":"score"})
    mapScores = []
    for mapDivScore in mapDivScores:
        mapScore = mapDivScore.text.strip()
        mapScores.append(int(mapScore))
    # mapScores = [mapDivScore.text.strip().split() for mapDivScore in mapDivScores]

    mapTSideScores = []
    mapCTSideScores = []

    for mapDivStatHeader in mapDivStatsHeaders:
        mapTSideScores.append([mapTScore.text for mapTScore in mapDivStatHeader.find_all("span", {"class":"mod-t"})])
        mapCTSideScores.append([mapCTScore.text for mapCTScore in mapDivStatHeader.find_all("span", {"class":"mod-ct"})])
    
    mapSideScores = []

    for mapNum in range(len(mapNames)):
        # print(mapNum, len(mapNames))
        for teamNum in range(2):
            mapSideScores.append([int(mapTSideScores[mapNum][teamNum]), int(mapCTSideScores[mapNum][teamNum])])
            # print()

    mapStatScores = []

    for i, name in enumerate(mapNames):
        start = i * 2
        end = start + 2

        scores = mapScores[start:end]
        side_scores = mapSideScores[start:end]

        mapStatScores.append([name, scores, side_scores])


    # mapSpanTSideScores = mapDivStatsHeader.find_all("span", {"class":"mod-t"})
    # mapSpanCTSideScores = mapDivStatsHeader.find_all("span", {"class":"mod-ct"})
    # mapTSideScores = [mapSpanTSideScore.text.strip() for mapSpanTSideScore in mapSpanTSideScores]
    # mapCTSideScores = [mapSpanCTSideScore.text.strip() for mapSpanCTSideScore in mapSpanCTSideScores]

    # print(mapScores, mapStatScores)

    return mapStatScores