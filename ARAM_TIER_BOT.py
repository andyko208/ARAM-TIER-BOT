import requests

import discord
from discord.ext import commands
from discord import File

# get your own api key from "https://developer.riotgames.com/"
g_api_key = "RGAPI-c879cd51-15bb-4144-afd3-fc484c3f7faa"
g_region = "na"
g_summoner_name = "le5le"
def get_encrypted():
    summonerSearchURL = "https://" + g_region + "1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + g_summoner_name + "?api_key=" + g_api_key
    response = requests.get(summonerSearchURL)
    responseJson = response.json()

    return responseJson['accountId']

# get_last_20_games
def get_tier(encId):
    matchSearchURL = "https://" + g_region + "1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + encId + "?api_key=" + g_api_key
    response = requests.get(matchSearchURL)
    responseJson = response.json()

    for matchId in responseJson['matches']:
        gameId = matchId['gameId']

        matchURL = "https://" + g_region + "1.api.riotgames.com/lol/match/v4/matches/" + str(gameId) + "?api_key=" + g_api_key

        response = requests.get(matchURL)
        responseJson = response.json()

        if responseJson['gameMode'] == "ARAM":
            if responseJson['teams'][0]['win'] == "Win":
                #['any data']
                print(responseJson['teams'][0]['win'])

# KDA/분당 DMG/ 골드획득량/ cs array, figure out how to check the chmaps that I played
# up to last 20 games
win = ['true', 'false']
kda = [3.5, 5.4, 6.0]
isSupport = ['true', 'false']
DPS = [1, 2, 3]
cs = [123, 456]

# find tier based on the data stores in array
def get_tier():

encId = get_encrypted()
get_tier(encId)
