import asyncio
import json
import random

import discord

import googleimages
from classes import Memo

client = discord.Client()
with open('credentials.json') as json_data:
    creds = json.load(json_data)
tell = []


@client.event
async def on_ready():
    random.seed()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    args = ()
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
    elif message.content.startswith('!memo'):
        tmp = await client.send_message(message.channel, 'Memo being processed...!')
        args = message.content.split(' ', 2)
        if len(args) != 3:
            await client.edit_message(tmp, 'Incorrect number of arguments provided.')
            return
        member = discord.utils.find(lambda m: m.name == args[1], message.channel.server.members)
        if member is not None:
            global tell
            memo = Memo(member, message.author, args[2], message.channel)
            tell.append(memo)
            await client.edit_message(tmp, 'Memo added for {}.'.format(memo.to))
        else:
            await client.edit_message(tmp, 'Failed to find a user with that username in the channel.')
    elif message.content.startswith('!help'):
        await client.send_message(message.channel, 'Help not received')
    elif message.content.startswith('!image'):
        tmp = await client.send_message(message.channel, 'Finding image...')
        args = message.content.split(' ', 1)
        (result, error) = googleimages.search(args[1], creds, 1)
        if error == 0:
            await client.edit_message(tmp, '{},\n{}'.format(message.author.mention, result))
        else:
            await client.edit_message(tmp, 'Error:\n{}'.format(result))
    elif message.content.startswith('!imager'):
        tmp = await client.send_message(message.channel, 'Finding image...')
        args = message.content.split(' ', 1)
        rand = random.randint(0, 9)
        (result, error) = googleimages.search(args[1], creds, rand)
        if error == 0:
            await client.edit_message(tmp, '{},\n{}'.format(message.author.mention, result))
        else:
            await client.edit_message(tmp, 'Error:\n{}'.format(result))


@client.event
async def on_member_update(before, after):
    global tell
    memos = []
    for _memo in tell:
        if _memo.to.id == after.id:
            memos.append(_memo)
    for memo in memos:
        if memo is not None:
            if after.server == memo.channel.server and after.status == 'online':
                tell.remove(memo)
                await client.send_message(memo.channel, "{}: {} sent you a message:\n```{}```".format(memo.to.mention,
                                                                                                      memo.sender.mention,
                                                                                                      memo.message))


@client.event
async def on_typing(channel, user, when):
    global tell
    memos = []
    for _memo in tell:
        if _memo.to.id == user.id:
            memos.append(_memo)
    for memo in memos:
        if memo is not None:
            if user.server == memo.channel.server:
                tell.remove(memo)
                await client.send_message(memo.channel, "{}: {} sent you a message:\n```{}```".format(memo.to.mention,
                                                                                                      memo.sender.mention,
                                                                                                      memo.message))


client.run(creds['token'])
