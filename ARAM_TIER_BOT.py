import requests

import discord
from discord.ext import commands
from discord import File

# get your own api key from "https://developer.riotgames.com/"
g_api_key = "RGAPI-45f99881-6c4b-4abf-a1fc-5317c7bf4e41"
g_region = "na"
g_summoner_name = "CRSXW"

# champs by champ id: http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/champion.json

# data that will be used to compute the tier
# Team data

# int
# in seconds ex) 1142
gameDuration = []

# String
# "Win" or "Fail"
win = []

# Player's champion data
# from getMatchData()
# int
championId = []
kills = []
deaths = []
assists = []
DmgToChamp = []
DmgToTurret = []
DmgTaken = []
totalGold = []
cs = []
supChampsId = []
# 1~18
champLV = []
# in seconds ex) 40
timeCCingOthers = []

# from isSupport()
supChampsId = []

##################################너가 할꺼 ########################################
# game duration, kills, deaths, assists 갖고 알아서
kda = []
# dmg per sec
DPS = []

# dmg per min
DPM = []

#gold per min
GPM = []
###################################################################################

# boolean
isSupChamp = []
isFirstBlood =[]
isFirstBloodassist=[]
isTriple = []
isQuadra = []
isPenta = []

def getEncryptedId():
    summonerSearchURL = "https://" + g_region + "1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + g_summoner_name + "?api_key=" + g_api_key
    response = requests.get(summonerSearchURL)
    responseJson = response.json()

    return responseJson['accountId']

# get_last_20_games
def getMatchData(encId):
    matchSearchURL = "https://" + g_region + "1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + encId + "?api_key=" + g_api_key
    response = requests.get(matchSearchURL)
    responseJson = response.json()

    nthGame = 0
    for matchInfo in responseJson['matches']:
        # print(matchInfo['gameId'])

        #print(len(kills))
        if len(kills) == 20:
            return
        gameId = matchInfo['gameId']
        myChampId = matchInfo['champion']

        # getting into the more details of the current match
        matchURL = "https://" + g_region + "1.api.riotgames.com/lol/match/v4/matches/" + str(gameId) + "?api_key=" + g_api_key
        response = requests.get(matchURL)
        responseJson = response.json()

        # Ignore other mathces than ARAM game mode
        if responseJson['gameMode'] == "ARAM":
            # blue team
            blueGameResult = responseJson['teams'][0]['win']
            # red team
            redGameResult = responseJson['teams'][1]['win']

            gameDuration.insert(nthGame, responseJson['gameDuration'])
            for participant in responseJson['participants']:
                if participant['championId'] == myChampId:
                    championId.insert(nthGame, participant['championId'])
                    if participant['teamId'] == 100:
                        win.insert(nthGame, blueGameResult)
                    else:
                        win.insert(nthGame, redGameResult)
                    kills.insert(nthGame, participant['stats']['kills'])
                    deaths.insert(nthGame,participant['stats']['deaths'])
                    assists.insert(nthGame,participant['stats']['deaths'])
                    DmgToChamp.insert(nthGame,participant['stats']['totalDamageDealtToChampions'])
                    DmgToTurret.insert(nthGame,participant['stats']['damageDealtToTurrets'])
                    DmgTaken.insert(nthGame,participant['stats']['totalDamageTaken'])
                    timeCCingOthers.insert(nthGame,participant['stats']['timeCCingOthers'])
                    totalGold.insert(nthGame,participant['stats']['goldEarned'])
                    cs.insert(nthGame,participant['stats']['totalMinionsKilled'])
                    champLV.insert(nthGame,participant['stats']['champLevel'])
                    isFirstBlood.insert(nthGame,participant['stats']['firstBloodKill'])
                    isFirstBloodassist.insert(nthGame,participant['stats']['firstBloodAssist'])
                    isTriple.insert(nthGame,participant['stats']['tripleKills'])
                    isQuadra.insert(nthGame,participant['stats']['quadraKills'])
                    isPenta.insert(nthGame,participant['stats']['pentaKills'])
                    nthGame += 1

    def getKDA():
        nthgame = 0
        for i in range(0,len(kills)):
            kda.insert(nthgame,(kills[i]+assists[i])/deaths[i])
            nthgame+=1

    def getDPS():
        nthgame = 0
        for i in range(0,len(DmgToChamp)):
            DPS.insert(nthgame,(DmgToChamp[i]/gameDuration[i]))
            nthgame+=1

    def getDPM():
        nthgame = 0
        for i in range(0,len(DPS)):
            DPM.insert(nthgame,DPS[i]*60)
            nthgame+=1
    def getGPM():
        nthgame = 0
        for i in range(0,len(gameDuration)):
            GPM.insert(nthgame,((totalGold[i]/gameDuration[i])*60))
            nthgame+=1



# KDA/분당 DMG/ 골드획득량/cs array
# up to last 20 games

# lulu
# leona
# blitzcrank
# morgana
# pantheon
# thresh
# bard
# rakan
# alistar
# lux
# zilean
# taric
# janna
# nautilus
# pyke
# sona
# soraka
# braum
# zyra
# karma
# nami

# do not exist in json file: http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/champion.json
# yuumi
# tahm kench

def isSupport():
    supChamps = ['Lulu', 'Leona' ,'Blitzcrank', 'Morgana', 'Pantheon', 'Thresh', 'Bard', 'Brand', 'Rakan', 'Alistar',
                'Lux', 'Zilean', 'Taric', 'Janna', 'Nautilus', 'Pyke', 'Sona', 'Soraka', 'Braum',
                'Zyra', 'Karma', 'Nami', 'Yuumi']

    champsURL = "http://ddragon.leagueoflegends.com/cdn/10.20.1/data/en_US/champion.json"
    response = requests.get(champsURL)
    responseJson = response.json()
    for champ in supChamps:
        supChampsId.append(int(responseJson['data'][champ]['key']))
        responseJson['data']
    for champ in championId:
        # print(champ)
        # print(supchampsId)supchampsId
        if champ in supchampsId:
            isSupChamp.append(True)
        else:
            isSupChamp.append(False)


##################################너가 할꺼 ########################################
def get_KDAscore (avg_KDA,isSupChamp):
        if bool(isSupChamp): #if it a support
            if avg_KDA > 5:
                total_val+=0.4
            elif avg_KDA > 4:
                total_val+=0.35
            elif avg_KDA > 3:
                total_val+=0.3
            elif avg_KDA > 2.5:
                total_val+=0.25
            elif avg_KDA > 2:
                total_val+=0.2
            elif avg_KDA > 1:
                total_val+=0.1
            else:
                total_val+=0.05
            if avg_fb > 10 or avg_fba > 14:
                total_val+=0.1
        else: #when its not support
            if avg_KDA > 4:
                total_val+=0.4
            elif avg_KDA > 3.5:
                total_val+=0.35
            elif avg_KDA > 3:
                total_val+=0.3
            elif avg_KDA > 2.5:
                total_val+=0.25
            elif avg_KDA > 2:
                total_val+=0.2
            elif avg_KDA > 1:
                total_val+=0.1
            else:
                total_val+=0.05
            if avg_fb > 13 or avg_fba > 15:
                total_val+=0.1
def get_GPMscore(avg_GPM):
    if avg_GPM > 640:
        total_val+=0.2
    elif avg_GPM > 620:
        total_val+=0.15
    elif avg_GPM > 600:
        total_val+=0.13
    elif avg_GPM > 580:
        total_val+=0.1
    elif avg_GPM > 560:
        total_val+=0.08
    elif avg_GPM > 540:
        total_val+=0.05
    else:
        total_val+=0.03
def get_DPMscore(avg_DPM,isSupChamp):
    if bool(isSupChamp):
        if avg_DPM > 1600:
            total_val+=0.3
        elif avg_DPM > 1550:
            total_val+=0.28
        elif avg_DPM > 1500:
            total_val+=0.25
        elif avg_DPM > 1450:
            total_val+=0.22
        elif avg_DPM > 1350:
            total_val+=0.18
        elif avg_DPM > 1200:
            total_val+=0.15
        else:
            total_val+=0.1
    else: #when its not support
        if avg_DPM > 1400:
            total_val+=0.3
        elif avg_DPM > 1350:
            total_val+=0.26
        elif avg_DPM > 1300:
            total_val+=0.22
        elif avg_DPM > 1250:
            total_val+=0.17
        elif avg_DPM > 1200:
            total_val+=0.15
        elif avg_DPM > 1100:
            total_val+=0.13
        else:
            total_val+=0.1

def tier_result(percent):
    if percent >95:
        return "Challenger"
    elif percent > 90:
        return "Grandmaster"
    elif percent > 85:
        return "Master"
    elif percent > 80:
        return "Diamond"
    elif percent > 75:
        return "Platinum"
    elif percent > 70:
        return "Gold"
    elif percent > 65:
        return "Silver"
    else:
        return "Bronze"

def computeTier():
    total_val = 0
    for i in range(0,len(KDA)):
        total_KDA += KDA[i]#kda
        total_DPM += DPM[i]#damamge
        total_GPM += GPM[i]#gold
        total_cs += cs[i]#cs

        avg_KDA = total_KDA/len(KDA)
        avg_DPM = total_DPM/len(DPM)
        avg_GPM = total_GPM/len(GPM)
        avg_cs = total_cs/len(cs)
        if isFirstBlood[i]:
            total_fb +=1
        if isFirstBloodassist[i]:
            total_fba +=1
        avg_fb =total_fb/len(isFirstBlood)
        avg_fba =total_fba/len(isFirstBloodassist)
        if(isPenta[i]==True):
            penta +=1
        if(isQuadra[i]==True):
            quadra +=1
        if(isTriple[i]==True):
            triple +=1

    total_val +=penta*0.1
    total_val +=quadra*0.05
    total_val +=triple*0.03

    get_KDAscore(avg_KDA,isSupChamp[i])
    get_GPMscore(avg_GPM)
    get_DPMscore(avg_DPM,isSupChamp[i])
    percent = total_val*100
    tier = tier_result(percent)








getMatchData(getEncryptedId())
isSupport()
# print("Champion Id: ")
# print(championId)
# print("Sup champs Id: ")
# print(supchampsId)
print("Sup champ bools`:")
print(isSupChamp)
# print(kills)
# print(deaths)
# print(assists)
# print(win)
