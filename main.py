import discord
from discord.ext import commands

import requests
import json
import urllib
import random

api_url = "https://api.jikan.moe/v4/anime"

# READ THE SUPER SECRET TOKEN
key_file = open("credentials/discord.token", "r", encoding='ascii')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents, debug_guilds=["1038312545813012480"])

def print_json(dict):
    json_object = json.dumps(dict, indent=4)
    print(json_object)

@bot.command(description='Search for a Voice Actor',)
async def va(ctx, *, arg=''):
    
    if arg == '':
        await ctx.send("Type a persón")
        return

    people_url = "https://api.jikan.moe/v4/people"
    payload = dict(q=arg, limit=1)
    urllib.parse.urlencode(payload)

    response = requests.get(people_url, params=payload)
    json_response = json.loads(response.text)
    person = json_response["data"][0]

    print_json(person)
    nameu = person["name"]
    pic = person["images"]["jpg"]["image_url"]

    embed=discord.Embed(title=nameu, color=0xFF5733, description = person["about"])
    embed.set_thumbnail(url=pic)
    embed.add_field(name = "Bday :D", value = person["birthday"])

    await ctx.send(embed=embed)

def get_url(url, load):
    print(url)
    response = requests.get(url, params=load)
    json_response = json.loads(response.text)
    print_json(json_response)
    return json_response["data"]


@bot.command(description='Search for a Character',)
async def char(ctx, *, arg=''):
    
    if arg == '':
        await ctx.send("Type a character")
        return

    people_url = "https://api.jikan.moe/v4/characters"
    payload = dict(q=arg, limit=1, order_by="favorites", sort="desc")
    urllib.parse.urlencode(payload)

    response = requests.get(people_url, params=payload)
    json_response = json.loads(response.text)

    if len(json_response["data"]) < 1:
        await ctx.send("No Results Found")
        return

    person = json_response["data"][0]
    nameu = person["name"]
    pic = person["images"]["jpg"]["image_url"]
    char_id = person["mal_id"]
    char_url = people_url + "/" + str(char_id) + "/full"
    character = get_url(char_url, dict())
    print_json(character)

    va = ""
    va_url = ""

    for v in character["voices"]:
        if v["language"] == "Japanese":
            va = v["person"]["name"]
            va_url = v["person"]["images"]["jpg"]["image_url"]
            break

    embed=discord.Embed(title=nameu, color=0xFF5733, description = person["about"])
    embed.set_thumbnail(url=pic)
    if va != "":
        embed.add_field(name="Voice Actor", value=va)
    if va_url:
        embed.set_image(url=va_url)

    await ctx.send(embed=embed)

# Return an embed with information about anime
def format_anime(anime):
    nameu = anime["title_japanese"]
    posteru = anime["images"]["jpg"]["image_url"]
    name = anime["title_english"]

    embed=discord.Embed(title=nameu, description=name, color=0xFF5733)
    embed.set_thumbnail(url=posteru)
    
    mal_id = anime["mal_id"]
    char_url = api_url + "/" + str(mal_id) + "/characters"
    response = requests.get(char_url)
    json_response = json.loads(response.text)
    characters = json_response["data"]

    for char in characters:
        ch = char["character"]["name"]
        va = ""

        for v in char["voice_actors"]:
            if v["language"] == "Japanese":
                va = v["person"]["name"]
                break

        embed.add_field(name=ch, value=va, inline=True)
    return embed

# /any command
@bot.command(description='Return a random animu',)
async def any(ctx, *, arg=''):

    # construct getTopAnime URL
    top_url = "https://api.jikan.moe/v4/top/anime"

    # make the parameter thinggies
    #    type (tv/movie/ova/special/ona/music)
    #    filter (airing/upcoming/bypopularity/favorite)
    #    rating (g/pg/pg13/r17/r/rx)
    #    sfw (true/false)
    #    page
    #    limit
    payload = dict(type="tv", limit=1000, filter="bypopularity", sfw=True)
    urllib.parse.urlencode(payload)

    # send the request
    response = requests.get(top_url, params=payload)

    # read the result for the user person i guess idk
    json_response = json.loads(response.text)
    anime = json_response["data"]

    # get a random number
    num = random.randint(0, len(anime) - 1)

    await ctx.send(str(num + 1) + ". " + anime[num]["title"])

# /mmb command
@bot.command(description='Return information about an anime',)
async def mmb(ctx, *, arg=''):

    if arg == '':
        await ctx.send("Type an anime name")
        return
    
    payload = dict(q=arg, limit=10, order_by="popularity", sort = "asc", type="tv")
    urllib.parse.urlencode(payload)
    
    response = requests.get(api_url, params=payload)
    json_response = json.loads(response.text)
    animu = json_response["data"]

    anime = animu[0]

    for a in animu:
        if a["popularity"] != 0:
            anime = a
            break

    await ctx.send(embed=format_anime(anime))

    #####################################################
    # Try to call getAnimePictures and show some pictures
    #####################################################
    #     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢲⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀       
    #     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    #     ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠄⠂⢉⠤⠐⠋⠈⠡⡈⠉⠐⠠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    #     ⠀⠀⠀⠀⢀⡀⢠⣤⠔⠁⢀⠀⠀⠀⠀⠀⠀⠀⠈⢢⠀⠀⠈⠱⡤⣤⠄⣀⠀⠀⠀⠀⠀
    #     ⠀⠀⠰⠁⠀⣰⣿⠃⠀⢠⠃⢸⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠈⢞⣦⡀⠈⡇⠀⠀⠀
    #     ⠀⠀⠀⢇⣠⡿⠁⠀⢀⡃⠀⣈⠀⠀⠀⠀⢰⡀⠀⠀⠀⠀⢢⠰⠀⠀⢺⣧⢰⠀⠀⠀⠀
    #     ⠀⠀⠀⠈⣿⠁⡘⠀⡌⡇⠀⡿⠸⠀⠀⠀⠈⡕⡄⠀⠐⡀⠈⠀⢃⠀⠀⠾⠇⠀⠀⠀⠀
    #     ⠀⠀⠀⠀⠇⡇⠃⢠⠀⠶⡀⡇⢃⠡⡀⠀⠀⠡⠈⢂⡀⢁⠀⡁⠸⠀⡆⠘⡀⠀⠀⠀⠀
    #     ⠀⠀⠀⠸⠀⢸⠀⠘⡜⠀⣑⢴⣀⠑⠯⡂⠄⣀⣣⢀⣈⢺⡜⢣⠀⡆⡇⠀⢣⠀⠀⠀⠀
    #     ⠀⠀⠀⠇⠀⢸⠀⡗⣰⡿⡻⠿⡳⡅⠀⠀⠀⠀⠈⡵⠿⠿⡻⣷⡡⡇⡇⠀⢸⣇⠀⠀⠀
    #     ⠀⠀⢰⠀⠀⡆⡄⣧⡏⠸⢠⢲⢸⠁⠀⠀⠀⠀⠐⢙⢰⠂⢡⠘⣇⡇⠃⠀⠀⢹⡄⠀⠀
    #     ⠀⠀⠟⠀⠀⢰⢁⡇⠇⠰⣀⢁⡜⠀⠀⠀⠀⠀⠀⠘⣀⣁⠌⠀⠃⠰⠀⠀⠀⠈⠰⠀⠀
    #     ⠀⡘⠀⠀⠀⠀⢊⣤⠀⠀⠤⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠄⠀⢸⠃⠀⠀⠀⠀⠀⠃⠀
    #     ⢠⠁⢀⠀⠀⠀⠈⢿⡀⠀⠀⠀⠀⠀⠀⢀⡀⠀⠀⠀⠀⠀⠀⢀⠏⠀⠀⠀⠀⠀⠀⠸⠀
    #     ⠘⠸⠘⡀⠀⠀⠀⠀⢣⠀⠀⠀⠀⠀⠀⠁⠀⠃⠀⠀⠀⠀⢀⠎⠀⠀⠀⠀⠀⢠⠀⠀⡇
    #     ⠀⠇⢆⢃⠀⠀⠀⠀⠀⡏⢲⢤⢀⡀⠀⠀⠀⠀⠀⢀⣠⠄⡚⠀⠀⠀⠀⠀⠀⣾⠀⠀⠀
    #     ⢰⠈⢌⢎⢆⠀⠀⠀⠀⠁⣌⠆⡰⡁⠉⠉⠀⠉⠁⡱⡘⡼⠇⠀⠀⠀⠀⢀⢬⠃⢠⠀⡆
    #     ⠀⢢⠀⠑⢵⣧⡀⠀⠀⡿⠳⠂⠉⠀⠀⠀⠀⠀⠀⠀⠁⢺⡀⠀⠀⢀⢠⣮⠃⢀⠆⡰⠀
    #     ⠀⠀⠑⠄⣀⠙⡭⠢⢀⡀⠀⠁⠄⣀⣀⠀⢀⣀⣀⣀⡠⠂⢃⡀⠔⠱⡞⢁⠄⣁⠔⠁⠀
    #     ⠀⠀⠀⠀⠀⢠⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⠉⠁⠀⠀⠀⠀
    #     ⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀
    #####################################################

    #    mal_id = anime["mal_id"]
    #    picture_url = api_url + "/" + str(mal_id) + "/pictures"
    #    response = requests.get(picture_url)
    #    json_response = json.loads(response.text)
    #
    #    print_json(json_response)
    #    for i in json_response["data"]:
    #        image = i["jpg"]["image_url"]
    #        await ctx.send(image)
    # image = json_response["data"][0]["jpg"]["image_url"]
    # await ctx.send(image)


@client.event
async def on_ready():
    print('We are logged in')

# Define message handler
#   This will check each message for /mmb (for meowmeowbeans)
@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if message.content.startswith('/mmb'):
        await message.channel.send('meowmeowbeans is alive')

bot.run(key_file.read())
#client.run(key_file.read())