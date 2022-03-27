import discord
from discord.ext import commands
from datetime import datetime
import csv
import tqdm
import tqdm.asyncio
from pathlib import Path
from dotenv import load_dotenv
from os import getenv

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
description = '''Discord Logger Bot'''
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='&', description=description, intents=intents)
TOKEN = getenv("DISCORD_TOKEN")


@bot.command(aliases=[], brief='Records information for each message in a server and join date and times for current '
                               'members')
async def audit(ctx):
    # Creating csv files
    serverName = ctx.message.guild.name
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
    filenameMessages = ".\\Logs\\" + f'{"messagesAudit_"}{serverName}{"_"}{dt_string}{".csv"}'
    fieldsMessages = ['Channel', 'Username', 'bot', "Admin", 'Reactions', 'Date', 'Time']
    with open(filenameMessages, 'w', newline='') as messagesCSV:
        csvWriterMessages = csv.writer(messagesCSV)
        csvWriterMessages.writerow(fieldsMessages)

    # Checking channels and storing information in csv files
    text_channel_list = []
    for channel in ctx.message.guild.text_channels:
        text_channel_list.append(channel)
    for a in text_channel_list:
        async for b in tqdm.asyncio.tqdm(a.history(limit=1000000)):
            # Hardcoded check for a role, current TA Check
            taCheck = False
            if str(type(b.author)) != "<class 'discord.user.User'>":
                for c in b.author.roles:
                    if str(c) == "admin":
                        taCheck = True
            if str(b.type) != 'MessageType.new_member':
                reactions = 0
                for c in b.reactions:
                    num = c.count
                    reactions += num
                messageInfo = [str(b.channel), str(b.author), str(b.author.bot), str(taCheck), str(reactions),
                               str(str(b.created_at).split(' ')[0]), str(str(b.created_at).split(' ')[1].split('.')[0])]
                with open(filenameMessages, 'a', newline='', encoding="utf-8") as messagesCSV:
                    csvWriterMessages = csv.writer(messagesCSV)
                    csvWriterMessages.writerow(messageInfo)

    # Logs current members join dates and times
    filenameJoins = ".\\Logs\\" + f'{"joinsAudit_"}{serverName}{dt_string}{".csv"}'
    fieldsJoins = ['Username', 'bot', 'Date', 'Time']
    with open(filenameJoins, 'w', newline='') as joinsCSV:
        csvWriterJoins = csv.writer(joinsCSV)
        csvWriterJoins.writerow(fieldsJoins)
    memberList = []
    for member in ctx.message.guild.members:
        memberList.append(member)
    for a in memberList:
        print(a)
        messageInfo = [str(a.display_name), str(a.bot), str(str(a.joined_at).split(' ')[0]),
                       str(str(a.joined_at).split(' ')[1].split('.')[0])]
        with open(filenameJoins, 'a', newline='', encoding="utf-8") as joinsCSV:
            csvWriterJoins = csv.writer(joinsCSV)
            csvWriterJoins.writerow(messageInfo)
    print("Done!")


@bot.command(aliases=[], brief='Retrieves the date and time each current member joined a server, done in Audit as well.')
async def joins(ctx):
    serverName = ctx.message.guild.name
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y__%H_%M_%S")
    filenameJoins = ".\\Logs\\" + f'{"joinsAudit_"}{serverName}{dt_string}{".csv"}'
    fieldsJoins = ['Username', 'bot', 'Date', 'Time']
    with open(filenameJoins, 'w', newline='') as joinsCSV:
        csvWriterJoins = csv.writer(joinsCSV)
        csvWriterJoins.writerow(fieldsJoins)
    memberList = []
    for member in ctx.message.guild.members:
        memberList.append(member)
    for a in memberList:
        print(a)
        messageInfo = [str(a.display_name), str(a.bot), str(str(a.joined_at).split(' ')[0]),
                       str(str(a.joined_at).split(' ')[1].split('.')[0])]
        with open(filenameJoins, 'a', newline='', encoding="utf-8") as joinsCSV:
            csvWriterJoins = csv.writer(joinsCSV)
            csvWriterJoins.writerow(messageInfo)


@bot.command(aliases=[], brief='Test function for debugging purposes')
async def test(ctx):
    text_channel_list = []
    for channel in ctx.message.guild.text_channels:
        text_channel_list.append(channel)
    for a in text_channel_list:
        async for b in tqdm.asyncio.tqdm(a.history(limit=1000000)):
            taCheck = False
            if str(type(b.author)) != "<class 'discord.user.User'>":
                for c in b.author.roles:
                    print(str(c))
                    if str(c) == "Admin":
                        taCheck = True
                print(taCheck)

bot.run(TOKEN)