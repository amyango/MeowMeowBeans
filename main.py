import discord

# test
def main():
    print("hello world")

    # READ THE SUPER SECRET TOKEN
    f = open("/workspaces/MeowMeowBeans/credentials/meowmeowbeans.token", "r")

    intents = discord.Intents.default()
    intents.members = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print('We are logged in')

    client.run(f.read())

main()