import requests

import discord
from discord.ext import commands
from discord import File

# get your own api key from "https://developer.riotgames.com/"
g_api_key = "RGAPI-2d4d982c-064d-4b70-948f-a7c98f0f3ef7"
g_region = "na"
g_summoner_name = "Stanza"

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
# 1~18
champLV = []
# in seconds ex) 40
timeCCingOthers = []

# from isSupport()
supChampsId = []

##################################너가 할꺼 ########################################
# game duration, kills, deaths, assists 갖고 알아서
KDA = []
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


def getName(region, summonerName, apiKey):
    summonerSearchURL = "https://" + region + "1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + apiKey
    print(summonerSearchURL)
    response = requests.get(summonerSearchURL)
    responseJson = response.json()
    print('In getName')
    print(responseJson)
    return responseJson['name']

def getProfileIcon(region, summonerName, apiKey):
    summonerSearchURL = "https://" + region + "1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + apiKey
    print(summonerSearchURL)
    response = requests.get(summonerSearchURL)
    responseJson = response.json()
    print('In getProfileIcon')
    print(responseJson)
    return responseJson['profileIconId']

def getEncryptedId(region, summonerName, apiKey):
    summonerSearchURL = "https://" + region + "1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName + "?api_key=" + apiKey
    print(summonerSearchURL)
    response = requests.get(summonerSearchURL)
    responseJson = response.json()
    print('In getEncryptedId')
    print(responseJson)
    return responseJson['accountId']

# get_last_20_games
def getMatchData(region, encId, apiKey, numGames):
    matchSearchURL = "https://" + region + "1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + encId + "?api_key=" + apiKey
    print(matchSearchURL)
    response = requests.get(matchSearchURL)
    responseJson = response.json()
    print(responseJson)

    nthGame = 0
    for matchInfo in responseJson['matches']:
        # print(matchInfo['gameId'])

        # Changed to 5 for easier testing
        if len(kills) == numGames:
            return
        gameId = matchInfo['gameId']
        myChampId = matchInfo['champion']

        # getting into the more details of the current match
        matchURL = "https://" + g_region + "1.api.riotgames.com/lol/match/v4/matches/" + str(gameId) + "?api_key=" + g_api_key
        response = requests.get(matchURL)
        responseJson = response.json()

        print("Gamemode: ")
        print(responseJson['gameMode'])
        # Ignore other mathces than ARAM game mode
        if responseJson['gameMode'] == "ARAM":
            # blue team
            blueGameResult = responseJson['teams'][0]['win']
            # red team
            redGameResult = responseJson['teams'][1]['win']

            gameDuration.insert(nthGame, responseJson['gameDuration'])
            for participant in responseJson['participants']:
                # print(participant)
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
            # print(kills)
            # print(assists)
            # print(deaths)

def getKDA():
    print("deaths:")
    print(deaths)
    print("kills:")
    print(kills)
    for i in range(len(kills)):
        print("kills at: " + str(i))
        print(kills[i])
        if kills[i] + assists[i] != 0:
            # perfect KDA
            if deaths[i] == 0:
                KDA.append(5)
            else:
                KDA.append((kills[i]+assists[i])/deaths[i])
        # user left at the beginning of the game / did not play the game properly
        else:
            KDA.append(0)
        # print(i)
        # print((kills[i]+assists[i])/deaths[i])
        # print(KDA)
def getDPM():

    for i in range(len(kills)):
        DPM.append((DmgToChamp[i]/gameDuration[i])*60)


def getGPM():

    for i in range(len(kills)):
        GPM.append((totalGold[i]/gameDuration[i])*60)






# up to last 10 games

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

    versionURL = "https://ddragon.leagueoflegends.com/api/versions.json"
    vResponse = requests.get(versionURL)
    vResponseJson = vResponse.json()
    mostRecentVersion = vResponseJson[0]

    champsURL = "http://ddragon.leagueoflegends.com/cdn/" + mostRecentVersion + "/data/en_US/champion.json"
    print(champsURL)
    response = requests.get(champsURL)
    responseJson = response.json()
    for champ in supChamps:
        supChampsId.append(int(responseJson['data'][champ]['key']))
        responseJson['data']
    for champ in championId:
        # print(champ)
        # print(supchampsId)supchampsId
        if champ in supChampsId:
            isSupChamp.append(True)
        else:
            isSupChamp.append(False)


################################## Joongwook ########################################
def get_winScore():
    total = 0
    for result in win:
        if result == "Win":
            total += 0.5 / len(win)
    print("total added:")
    print(total)
    return total

def get_KDAscore (avg_KDA, isSupChamp):
        if bool(isSupChamp): #if it a support
            if avg_KDA > 5:
                return 0.4
            elif avg_KDA > 4:
                return 0.35
            elif avg_KDA > 3:
                return 0.3
            elif avg_KDA > 2.5:
                return 0.25
            elif avg_KDA > 2:
                return 0.2
            elif avg_KDA > 1:
                return 0.1
            elif avg_KDA > 0.1:
                return 0.05
            else:
                return 0.001
        else: #when its not support
            if avg_KDA > 4:
                return 0.4
            elif avg_KDA > 3.5:
                return 0.35
            elif avg_KDA > 3:
                return 0.3
            elif avg_KDA > 2.5:
                return 0.25
            elif avg_KDA > 2:
                return 0.2
            elif avg_KDA > 1:
                return 0.1
            else:
                return 0.05
def get_GPMscore(avg_GPM):
    if avg_GPM > 720:
        return 0.3
    elif avg_GPM > 680:
        return 0.25
    elif avg_GPM > 630:
        return 0.2
    elif avg_GPM > 560:
        return 0.15
    elif avg_GPM > 540:
        return 0.1
    elif avg_GPM > 500:
        return 0.05
    else:
        return 0.03
def get_DPMscore(avg_DPM,isSupChamp):
    if bool(isSupChamp):
        if avg_DPM > 1400:
            return 0.3
        elif avg_DPM > 1350:
            return 0.26
        elif avg_DPM > 1300:
            return 0.22
        elif avg_DPM > 1250:
            return 0.17
        elif avg_DPM > 1200:
            return 0.15
        elif avg_DPM > 1100:
            return 0.13
        else:
            return 0.1

    else: #when its not support
        if avg_DPM > 1800:
            return 0.3
        elif avg_DPM > 1700:
            return 0.26
        elif avg_DPM > 1600:
            return 0.22
        elif avg_DPM > 1500:
            return 0.17
        elif avg_DPM > 1400:
            return 0.13
        elif avg_DPM > 1200:
            return 0.1
        else:
            return 0.05

def tier_result(percent):
    if percent > 95:
        return "Challenger"
    elif percent > 90:
        return "Grandmaster"
    elif percent > 85:
        return "Master"
    elif percent > 80:
        if percent > 84:
            return "Diamond 1"
        if percent > 83:
            return "Diamond 2"
        if percent > 82:
            return "Diamond 3"
        else:
            return "Diamond 4"
    elif percent > 75:
        if percent > 79:
            return "Platinum 1"
        if percent > 78:
            return "Platinum 2"
        if percent > 77:
            return "Platinum 3"
        else:
            return "Platinum 4"
    elif percent > 70:
        if percent > 74:
            return "Gold 1"
        if percent > 73:
            return "Gold 2"
        if percent > 72:
            return "Gold 3"
        else:
            return "Gold 4"
    elif percent > 65:
        if percent > 69:
            return "Silver 1"
        if percent > 68:
            return "Silver 2"
        if percent > 67:
            return "Silver 3"
        else:
            return "Silver 4"
    elif percent > 60:
        if percent > 64:
            return "Bronze 1"
        if percent > 63:
            return "Bronze 2"
        if percent > 62:
            return "Bronze 3"
        else:
            return "Bronze 4"
    # percent > 55
    else:
        if percent > 59:
            return "Iron 1"
        if percent > 58:
            return "Iron 2"
        if percent > 57:
            return "Iron 3"
        else:
            return "Iron 4"


# make calculation more precise with figuring out how to add kill participation
def computeTier(summonerName, numGames):
    # print('Computing tier for: ' + summonerName)
    getMatchData(g_region, getEncryptedId(g_region, summonerName, g_api_key), g_api_key, numGames)
    isSupport()
    # KDA = [3.0,3.0,6.0]
    # DPM = [1500,1400,1449]
    # GPM = [600,700,800]
    # isFirstBlood = [True,True,True]
    #isFirstBloodassist = [True,True,True]
    #isPenta = [False,False,True]
    #isQuadra = [False,False,True]
    #isTriple = [False,False,True]
    #isSupChamp = [False,False,False]
    total_val = 0
    total_fb = 0
    total_fba = 0
    penta = 0
    quadra = 0
    triple = 0
    total_KDA = 0
    total_DPM = 0
    total_GPM = 0
    avg_fb=0
    avg_fba=0
    if len(kills) > 0:
        getKDA()
        print(KDA)
        getDPM()
        print(DPM)
        getGPM()
        print(GPM)
        for i in range(0,len(KDA)):
            total_GPM += GPM[i] #gold
            #total_cs += cs[i]#cs
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
            total_KDA+=get_KDAscore(KDA[i],isSupChamp[i])
            total_DPM+=get_DPMscore(DPM[i],isSupChamp[i])
        if avg_fb > (len(KDA)/2) or avg_fba > 14:
            return 0.1

        avg_DPM= total_DPM/len(DPM)
        avg_GPM = total_GPM/(len(GPM))
        avg_KDA = total_KDA/(len(KDA))
        #avg_cs = total_cs/len(cs)
        total_val +=penta*0.05
        total_val +=quadra*0.03
        total_val +=triple*0.01
        total_val += avg_KDA+avg_DPM
        print("avg_KDA+avg_DPM")
        print((avg_KDA+avg_DPM) * 100)
        total_val+= get_GPMscore(avg_GPM)
        total_val+= get_winScore()/len(win)

        percent = total_val*100
        print(percent)
        tier = tier_result(percent)
        return tier
    # have not played any ARAM games during the season
    return "Unranked"



###########################################################################################




# print(computeTier(g_summoner_name, 5))
# getMatchData(g_region, getEncryptedId(g_region, g_summoner_name, g_api_key), g_api_key)
# isSupport()
# print(computeTier())
# get_winScore()


# print("Champion Id: ")
# print(championId)
# print("Sup champs Id: ")
# print(supchampsId)
#print("Sup champ bools`:")
#print(isSupChamp)
# print(kills)
# print(deaths)
# print(assists)
# print(win)
