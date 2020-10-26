import requests
from data_fetch import getMatchData, getEncryptedId, isSupport, computeTier, getProfileIcon, getName

import discord
from discord.ext import commands
from discord import File

g_api_key = "RGAPI-2d4d982c-064d-4b70-948f-a7c98f0f3ef7"
g_region = "NA"
g_summoner_name = ""

# getMatchData(g_region, getEncryptedId(g_region, g_summoner_name, g_api_key), g_api_key)
# isSupport()
# print("Current tier:")
# print(computeTier())

TOKEN = 'NzY4MTkxNDI1NTYwMDUxNzMz.X484BA.fIVT0u4VhysosaZs43wvsNOBwlI'

client = commands.Bot(command_prefix = '.')

client.remove_command('help')

@client.event
async def on_ready():
    print('hello')

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    help_embed = discord.Embed(
        colour = discord.Colour.orange()
    )

    help_embed.set_author(name='Commands:')
    help_embed.add_field(name='.aram {summoner name}', value='ex) .aram Hide on bush\nSelects a summoner to display stats for')
    help_embed.add_field(name='.region', value='Current search region set to')
    help_embed.add_field(name='.region {region name}', value='ex) .region NA\n Selects a server to search the summoner from')

    await ctx.send(embed=help_embed)

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
async def aram(ctx, summoner_name):
    embed_title = ""
    tiers = ['//cdn.lolchess.gg/images/lol/tier/provisional.png', '//cdn.lolchess.gg/images/lol/tier/iron_1.png',
    '//cdn.lolchess.gg/images/lol/tier/bronze_1.png', '//cdn.lolchess.gg/images/lol/tier/silver_1.png',
    '//cdn.lolchess.gg/images/lol/tier/gold_1.png', '//cdn.lolchess.gg/images/lol/tier/platinum_1.png',
    '//cdn.lolchess.gg/images/lol/tier/diamond_1.png', '//cdn.lolchess.gg/images/lol/tier/master_1.png',
    '//cdn.lolchess.gg/images/lol/tier/grandmaster_1.png', '//cdn.lolchess.gg/images/lol/tier/challenger_1.png']

    # actual summoner name from the game
    summonerName = getName(g_region, summoner_name, g_api_key)
    # summoner icon of the profile
    iconId = getProfileIcon(g_region, summoner_name, g_api_key)
    # embed.set_image(url='https://ddragon.leagueoflegends.com/cdn/10.10.3208608/img/item/3040.png')

    # let user calculate however many games as they want to display tiers for
    tier = computeTier(summonerName, 5)
    print(tier)
    embed_title = tier
    description = ""
    tier_img = ""

    # in the future, incoroprate ML and find out the play style of the player, and give custom messages that is meaning to them
    if "Challenger" in tier:
        tier_img = 'https:' + tiers[9]
        description = "Godlike player."
    elif "Grandmaster" in tier:
        tier_img = 'https:' + tiers[8]
        description = "Legendary player."
    elif "Master" in tier:
        tier_img = 'https:' + tiers[7]
        description = "Almost there."
    elif "Diamond" in tier:
        tier_img = 'https:' + tiers[6]
        description = "Afk will result in a substantial decrease in tiers."
    elif "Platinum" in tier:
        tier_img = 'https:' + tiers[5]
        description = "First blood means a lot."
    elif "Gold" in tier:
        tier_img = 'https:' + tiers[4]
        description = "Assists are as important as assists."
    elif "Silver" in tier:
        tier_img = 'https:' + tiers[3]
        description = "Try to avoid having deaths as possible."
    elif "Bronze" in tier:
        tier_img = 'https:' + tiers[2]
        description = "Playing for the team will be rewarding."
    elif "Iron" in tier:
        tier_img = 'https:' + tiers[1]
        description = "You can auto attack others with your left mouse click."
    # unranked
    else:
        tier_img = 'https:' + tiers[0]
        description = "Play games to find your tier!"

    print("tier_img")
    print(tier_img)
    print("embed_title")
    print(embed_title)
    first_ten = discord.Embed(
        title = embed_title,
        description = description,
        colour = discord.Colour.blue()
    )

    first_ten.set_author(name=summonerName, icon_url=f'http://ddragon.leagueoflegends.com/cdn/10.21.1/img/profileicon/{iconId}.png')
    first_ten.set_thumbnail(url=tier_img)


    await ctx.send(embed=first_ten)

client.run(TOKEN)
