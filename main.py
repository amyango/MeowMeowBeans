import discord
from discord.ext import commands

# test
print("hello world")

# READ THE SUPER SECRET TOKEN
key_file = open("/workspaces/MeowMeowBeans/credentials/meowmeowbeans.token", "r", encoding='ascii')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='/', intents=intents, debug_guilds=["1038312545813012480"])

@bot.command(description='Hello this is MeowMeowbeans',)
async def mmb(ctx, arg=''):
    await ctx.send(ctx.guild.id)
    if arg == '':
        await ctx.send("Type an anime name")

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