import os
import discord
from mcstatus import MinecraftServer

client = discord.Client()
bot_token = os.environ['DISCORD_TOKEN']
server = MinecraftServer(os.environ['MC_SERVER'], 25565)


@client.event
async def on_ready():
    print('Bot {0} is online'.format(client.user))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/server'):
        try:
            await message.channel.send("Server online with {0} players".format(server.status().players.online))
        except:
            await message.channel.send("Server offline")

client.run(bot_token)
