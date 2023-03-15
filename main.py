import discord
from discord.ext import commands

import requests
import json
import urllib

api_url = "https://api.jikan.moe/v4/anime"

# test
print("hello world")

# READ THE SUPER SECRET TOKEN
key_file = open("/workspaces/MeowMeowBeans/credentials/meowmeowbeans.token", "r", encoding='ascii')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents, debug_guilds=["1038312545813012480"])

@bot.command(description='Hello this is MeowMeowbeans',)
async def mmb(ctx, arg=''):

    if arg == '':
        await ctx.send("Type an anime name")
        return
    
    # We need to fix how it picks the top result
    # Also it can't handle multiple words at a time... not sure why
    payload = dict(q=arg, limit=1, order_by="popularity", sort = "asc", type="tv")
    urllib.parse.urlencode(payload)
    
    response = requests.get(api_url, params = payload)
    json_response = json.loads(response.text)
    animu = json_response["data"]

    #ama is very cool and she wrote cool code
    #RACHIE WROTE 99% OF THE CODE 
    #LIES
    nameu = animu[0]["title_japanese"]
    posteru = animu[0]["images"]["jpg"]["image_url"]
    name = animu[0]["title_english"]

    await ctx.send(nameu)
    await ctx.send(posteru)
    await ctx.send(name)

    mal_id = animu[0]["mal_id"]
    char_url = api_url + "/" + str(mal_id) + "/characters"
    response = requests.get(char_url)
    json_response = json.loads(response.text)
    char = json_response["data"]
    await ctx.send(char[0]["character"]["name"])
    await ctx.send(char[0]["character"]["images"]["jpg"]["image_url"])

    #get japanese voice actor (rachie hates the english)

    await ctx.send(char[0]["voice_actors"][0]["person"]["name"])
    await ctx.send(char[0]["voice_actors"][0]["person"]["images"]["jpg"]["image_url"])

    # Let us pick a specific character in the animu so rachie can see her
    # favorite hot ones
    
    #search for seiyuu uwu

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

# Connect to Kitsu Anime API thinggy
#   This will let us search for Animus that the user wants to look at

bot.run(key_file.read())
#client.run(key_file.read())