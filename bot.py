import requests
from data_fetch import getMatchData, getEncryptedId, isSupport, computeTier, getProfileIcon, getName

import discord
from discord.ext import commands
from discord import File

g_api_key = "RGAPI-2d4d982c-064d-4b70-948f-a7c98f0f3ef7"
g_region = "na"
g_summoner_name = ""

# getMatchData(g_region, getEncryptedId(g_region, g_summoner_name, g_api_key), g_api_key)
# isSupport()
# print("Current tier:")
# print(computeTier())

TOKEN = 'NzY4MTkxNDI1NTYwMDUxNzMz.X484BA.-mS0UYYYI1_qKTZT3vP_nU-XhmM'

client = commands.Bot(command_prefix = '.')

client.remove_command('help')

@client.event
async def on_ready():
    print('hello')

@client.command(aliases=['region', 'r'])
async def set_region(ctx, *args):
    global g_region
    if not args:
        await ctx.send(f'Current search region: {g_region}')
        return
    else:
        new_region = args[0].upper()
        valid_region = {'BR', 'EUNE', 'EUW', 'JP', 'KR', 'LAN', 'LAS', 'NA', 'OCE',
        'TR', 'RU'}
        if new_region in valid_region:
            g_region = new_region
            await ctx.send(f'Search region set to: {g_region}')
            return
    await ctx.send('Invalid region!')

@client.command()
# Using, https://ddragon.leagueoflegends.com/api/versions.json, always make fetch the data up-to-date patch version
async def aram(ctx, *, summoner_name):
    embed_title = ""
    tiers = ['//cdn.lolchess.gg/images/lol/tier/iron_1.png', '//cdn.lolchess.gg/images/lol/tier/bronze_1.png', '//cdn.lolchess.gg/images/lol/tier/silver_1.png',
    '//cdn.lolchess.gg/images/lol/tier/gold_1.png', '//cdn.lolchess.gg/images/lol/tier/platinum_1.png', '//cdn.lolchess.gg/images/lol/tier/diamond_1.png',
    '//cdn.lolchess.gg/images/lol/tier/master_1.png', '//cdn.lolchess.gg/images/lol/tier/grandmaster_1.png', '//cdn.lolchess.gg/images/lol/tier/challenger_1.png']

    # actual summoner name from the game
    summonerName = getName(g_region, summoner_name, g_api_key)
    # summoner icon of the profile
    iconId = getProfileIcon(g_region, summoner_name, g_api_key)
    # embed.set_image(url='https://ddragon.leagueoflegends.com/cdn/10.10.3208608/img/item/3040.png')
    tier = computeTier(summonerName)
    print(tier)
    tier_img = ""
    # bronze 1
    # if tier > 50 & tier < 55:
    #     tier_img = 'https:' + tiers[0]
    #     embed_title = "Bronze 1"
    # # silver 1
    # if tier > 50 & tier < 55:
    #     tier_img = 'https:' + tiers[0]
    #     embed_title = "Silver 1"
    # # gold 1
    # if tier > 50 & tier < 55:
    #     tier_img = 'https:' + tiers[0]
    #     embed_title = "Gold 1"
    # # plat 1
    # if tier > 50 & tier < 55:
    #     tier_img = 'https:' + tiers[0]
    #     embed_title = "Platinum 1"
    # # dia 1
    # if tier > 50 & tier < 55:
    #     tier_img = 'https:' + tiers[0]
    #     embed_title = "Diamond 1"
    # # master
    # if tier > 50 & tier < 55:
    #     tier_img = 'https:' + tiers[0]
    #     embed_title = "Master"
    if tier == "Bronze":
        tier_img = 'https:' + tiers[6]
        embed_title = "Master"

    print("tier_img")
    print(tier_img)
    print("embed_title")
    print(embed_title)
    first_ten = discord.Embed(
        title = embed_title,
        description = 'From the most recent matches',
        colour = discord.Colour.blue()
    )
    first_ten.set_author(name=summonerName, icon_url=f'http://ddragon.leagueoflegends.com/cdn/10.21.1/img/profileicon/{iconId}.png')
    first_ten.set_thumbnail(url=tier_img)
    # embed.set_footer(text='Click to load next five games')
    # print(tiers[0])
    print('reached here')
    await ctx.send(embed=first_ten)

client.run(TOKEN)
