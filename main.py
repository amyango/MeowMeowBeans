import discord
from discord.ext import commands

import requests
import json
import urllib
import random
import asyncio

# Variables
api_url = "https://api.jikan.moe/v4/anime"
pointsBook = {}
characterList = {}
sortedCharacterList = []
current_anime = ""
posteru = ""
characterlist_msg = None

# READ THE SUPER SECRET TOKEN
key_file = open("credentials/discord.token", "r", encoding='ascii')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents, debug_guilds=["1038312545813012480"])

def print_json(dict):
    json_object = json.dumps(dict, indent=4)
    print(json_object)

# TODO: Prettify the result points board
# TODO: Sort characters by popularity
# TODO: make mention work (might be able to do @<userid>)
# TODO: LET US CANCEL GAMES IN PROGRESS/SKIP ANIMUS WE DONT KNOW
# TODO: Variable game length
# TODO: Reveal all of them at the end
def set_characterlist(characters):
    global characterList
    characterList = {}
    for char in characters:
        charname = char["character"]["name"]
        characterList[charname] = Character(charname)

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

class Character:
    def __init__(self, name):
        self.name = name
        self.guessed = False
        self.whoGuessed = "unguessed"

    def __str__(self):
        if self.guessed:
            return self.name

        result=""
        for subname in self.name.split():
            result = result + ('x' * len(subname)) + " "
        return result

def print_characterlist():

    embed=discord.Embed(title=current_anime, description=current_anime, color=0xFF5733)
    embed.set_thumbnail(url=posteru)
    
    i=0
    for character in characterList:
        if i > 41:
            break

        char = characterList[character]

        embed.add_field(name=str(char), value=char.whoGuessed, inline=True)
        i += 1
    return embed

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

    i=0
    for char in characters:
        if i > 41:
            break
        ch = char["character"]["name"]
        va = ""

        for v in char["voice_actors"]:
            if v["language"] == "Japanese":
                va = v["person"]["name"]
                break

        embed.add_field(name=ch, value=va, inline=True)
        i += 1
    return embed

# /points command
@bot.command(description='Show user point totals',)
async def points(ctx, *, arg=''):
    # Returns how many points all the users have
    await ctx.send(str(pointsBook))

# /any command
@bot.command(description='Return a random animu',)
async def any(ctx, *, arg=''):

    # construct getTopAnime URL
    top_url = "https://api.jikan.moe/v4/top/anime"

    # get a random number
    num = random.randint(0, 99)
    pageNum = ((num-1)//25) + 1
    num2 = num%25
    # 24 = page 1
    # 25 = page 1
    # 26 = page 2

    # make the parameter thinggies
    # print(json_response)
    #    type (tv/movie/ova/special/ona/music)
    #    filter (airing/upcoming/bypopularity/favorite)
    #    rating (g/pg/pg13/r17/r/rx)
    #    sfw (true/false)
    #    page
    #    limit
    payload = dict(type="tv", limit=25, filter="bypopularity", sfw=True, page=pageNum)
    urllib.parse.urlencode(payload)

    # send the request
    response = requests.get(top_url, params=payload)

    # read the result for the user person i guess idk
    json_response = json.loads(response.text)

    if not "data" in json_response:
        await ctx.send("sad life it failed - probably got rate limited o:")
        print(json_response)
        return

    anime = json_response["data"]
    resultString = str(num + 1) + ") " + anime[num2]["title"]  + "\n" + anime[num2]["title_english"] 

    global current_anime
    current_anime = anime[num2]["title_english"]

    global posteru
    posteru = anime[num2]["images"]["jpg"]["image_url"]

    await ctx.send(resultString + "\nTELL ME SOME CHARACTERS\n")

    # Getting the list of characters
    mal_id = anime[num2]["mal_id"]
    char_url = api_url + "/" + str(mal_id) + "/characters"
    response = requests.get(char_url)
    json_response = json.loads(response.text)
    characters = json_response["data"]

    set_characterlist(characters)

    global characterlist_msg
    characterlist_msg = await ctx.send(embed=print_characterlist())

    for char in characters:
        ch = char["character"]["name"]
        va = ""

        for v in char["voice_actors"]:
            if v["language"] == "Japanese":
                va = v["person"]["name"]
                break
        #embed.add_field(name=ch, value=va, inline=True)

    # Waiting for people to tell us chracters in the list

    # implement checkCharacter(character, anime) -- should return true/false if the character is in that anime
    # implement points() -- keep track of how many characters a user got correct
    # return an embed with all of the characters (crossed out if someone got it right)
    # return who won and with how many points
    # allow 30 seconds for people to answer
    #       Probably don't allow anyone to start the game again if one is already going on

# characterList: list of Character objects
# Character Object:
#    [Character            ]
#    [  name: "All Might"  ]
#    [  guessed: True      ]
#    [  whoguessed: Yo Mama]
# If you print when guessed is true, it prints the name
# If you print when guessed is false, it prints all x's
def checkCharacter(character, characterList):
    for key in characterList:
        char = characterList[key]
        
        if char.guessed:
            continue
        foundMatchThisLoop = False
        foundWrongWord = False
        character = character.replace(",", "")

        ch = char.name
        ch = ch.replace(",", "")
        va = ""

        if ch.lower() == character.lower():
            return char

        for othername in character.split(" "):
            for name in ch.split(" "):
                if name.lower() == othername.lower():
                    foundMatchThisLoop = True
            if not foundMatchThisLoop:
                foundWrongWord = True
            foundMatchThisLoop = False # Reset this for the next word that the user typed in

        if not foundWrongWord:
            return char

    return None

# /mmb command
@bot.command(description='Return information about an anime',)
async def check(ctx, *, arg=''):
    if arg == '':
        await ctx.send("Type a character in my hero aca")
        return
    
    global current_anime
    if current_anime == "":
        await ctx.send("No game running, start one with /start")
        return
    
#    # Getting the list of characters
#    mal_id = "31964"
#    char_url = api_url + "/" + str(mal_id) + "/characters"
#    response = requests.get(char_url)
#    json_response = json.loads(response.text)
#    characters = json_response["data"]

    # Waiting for people to tell us chracters in the list
    result = checkCharacter(arg, characterList)
    if result != None:
        if str(ctx.author.name) in pointsBook:
            pointsBook[str(ctx.author.name)] += 1
        else:
            pointsBook[str(ctx.author.name)] = 1
        result.guessed = True
        result.whoGuessed = ctx.author.name
        await ctx.send("FOUND " + result.name)
        # await ctx.send(embed=print_characterlist())
        await characterlist_msg.edit(embed=print_characterlist())
    else:
        await ctx.send("NOT FOUND " + arg)
    
#only allow characters once
#only one game at a time
#implement random thingy
#use embeds
#detect ties
#use userid to index into map, keep both points and username

@bot.command(description='start a game',)
async def start(ctx, *, arg=''):

    global current_anime

    # clear all the points
    global pointsBook
    pointsBook = {}

    # get a random animu
    await any(ctx)

    # tell the people how long the game will last
    id = await ctx.send("You have 60 seconds to name as many characters as you can")
    print(id)
    print(id.id)

    anime = current_anime

    # sleep for that long
    await asyncio.sleep(60)

    if current_anime != anime:
        print("returning early - " + anime + " != " + current_anime)
        return

    # declare the winner/show the point totals
    winner = ""

    for person in pointsBook:
        if (winner == "") or (pointsBook[person] > pointsBook[winner]):
            winner = person

    if winner == "":
        await ctx.send("No winner, you all suck. Watch more anime. Weeb card revoked.")
        return

    embed=discord.Embed(title=":crown: " + winner + " - " + str(pointsBook[winner]), color=0xa9d9c6)
    for person in pointsBook:
        if person != winner:
             embed.add_field(name=person + " - " + str(pointsBook[person]), value="", inline=False)

    global msg_id
    msg_id = await ctx.send(embed=embed)

    print(msg_id)

    current_anime = ""

    #await ctx.send(str(pointsBook))
    #await ctx.send("The winner is @" + winner + "!!!!")

# /mmb command
@bot.command(description='Return information about an anime',)
async def stop(ctx, *, arg=''):
    global current_anime
    current_anime = ""
    return

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

    if message.content.startswith('test'):
        await message.channel.send('test passed')

    if message.content.startswith('/mmb'):
        await message.channel.send('meowmeowbeans is alive')

#@bot.event
#async def on_ready():
#    print('Online')
#
#@bot.event
#async def on_message(message):
#    print('Message')

bot.run(key_file.read())
#client.run(key_file.read())