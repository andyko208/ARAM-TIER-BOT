import requests

import discord
from discord.ext import commands
from discord import File

# get your own api key from "https://developer.riotgames.com/"
g_api_key = "RGAPI-4646500c-a2c1-4c3f-9141-66a3dd8fc876"
g_region = "na"
g_summoner_name = "stanza"

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

##################################너가 할꺼 ########################################
# game duration, kills, deaths, assists 갖고 알아서
kda = []
# dmg per sec
DPS = []
# dmg per min
DPM = []
###################################################################################

# boolean
isSupChamp = []
isFirstBlood =[]

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

        print(len(kills))
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
                    nthGame += 1


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
supchampsId = []
def isSupport():
    supChamps = ['Lulu', 'Leona' ,'Blitzcrank', 'Morgana', 'Pantheon', 'Thresh', 'Bard', 'Rakan', 'Alistar',
                'Lux', 'Zilean', 'Taric', 'Janna', 'Nautilus', 'Pyke', 'Sona', 'Soraka', 'Braum',
                'Zyra', 'Karma', 'Nami']

    champsURL = "http://ddragon.leagueoflegends.com/cdn/9.3.1/data/en_US/champion.json"
    response = requests.get(champsURL)
    responseJson = response.json()
    for champ in supChamps:
        supchampsId.append(int(responseJson['data'][champ]['key']))
        responseJson['data']
    for champ in championId:
        # print(champ)
        # print(supchampsId)
        if champ in supchampsId:
            isSupChamp.append(True)
        else:
            isSupChamp.append(False)


##################################너가 할꺼 ########################################
def computeTier():
    # Computes the tier based on arrays filled with datas, up to last 20 games throughout the season
    # the most recent match's kill obtained by the player's champ would be kills[0]


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
