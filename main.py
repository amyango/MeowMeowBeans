import discord




# test
def main():
    """This is a docstring"""
    print("hello world")

    # READ THE SUPER SECRET TOKEN
    key_file = open("/workspaces/MeowMeowBeans/credentials/meowmeowbeans.token", "r", encoding='ascii')

    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('We are logged in')

    client.run(key_file.read())

    # Define message handler
    #   This will check each message for /mmb (for meowmeowbeans)

    # Connect to Kitsu Anime API thinggy
    #   This will let us search for Animus that the user wants to look at

main()
