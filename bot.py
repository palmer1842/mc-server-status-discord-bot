import os
import json
import discord
from mcstatus import MinecraftServer

client = discord.Client()
bot_token = os.environ['DISCORD_TOKEN']
server = MinecraftServer(os.environ['MC_SERVER'], 25565)
# retrieve map of usernames to real names
with open('names.txt', 'r') as file:
    real_names = json.load(file)


@client.event
async def on_ready():
    print('Bot {0} is online'.format(client.user))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!server'):
        args = message.content.split()
        try:
            # query server
            query = server.query()
            current_players = query.players.online
            max_players = query.players.max
            online_players = query.players.names

            # return status and list of players
            if len(args) == 1:
                response = 'Server online with {0} of {1} players'.format(current_players, max_players)
                i = 1
                for player in online_players:
                    if i == 1:
                        response += ": " + real_names[player]
                    else:
                        if len(online_players) == 2:
                            response += " and " + real_names[player]
                        else:
                            if i == len(online_players):
                                response += ", and " + real_names[player]
                            else:
                                response += ", " + real_names[player]
                    i += 1
                await message.channel.send(response)
        except:
            await message.channel.send("Server offline")

client.run(bot_token)
