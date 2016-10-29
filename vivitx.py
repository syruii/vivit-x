import asyncio
import json
import random
import re
from hashlib import md5

import discord

import danbooru
import gelbooru
import googleimages
import quotes
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


# TODO: Learn how to asyncio properly
@client.event
async def on_message(message):
    args = ()
    if message.content.startswith('-test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))

    elif message.content.startswith('-sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    elif message.content.startswith('-memo'):
        tmp = await client.send_message(message.channel, 'Memo being processed...!')
        args = message.content.split(' ', 2)
        if len(args) != 3:
            await client.edit_message(tmp, 'Incorrect number of arguments provided.')
            return
        args[1],
        member = discord.utils.find(lambda m: m.name == args[1], message.channel.server.members)
        if member is not None:
            global tell
            memo = Memo(member, message.author, args[2], message.channel)
            tell.append(memo)
            await client.edit_message(tmp, 'Memo added for {}.'.format(memo.to))
        else:
            await client.edit_message(tmp, 'Failed to find a user with that username in the channel.')

    elif message.content.startswith('-help'):
        await client.send_message(message.channel, 'Help not received')

    elif message.content.startswith('-image'):
        tmp = await client.send_message(message.channel, 'Finding image...')
        args = message.content.split(' ', 1)
        if len(args) != 2:
            await client.edit_message(tmp, 'Error: Parameter required.')
            return
        (result, error) = googleimages.search(args[1], creds)
        if error == 0:
            await client.edit_message(tmp, '{},\n{}'.format(message.author.mention, result))
        else:
            await client.edit_message(tmp, 'Error:\n{}'.format(result))
    elif message.content.startswith('-rimage'):
        tmp = await client.send_message(message.channel, 'Finding image...')
        args = message.content.split(' ', 1)
        if len(args) != 2:
            await client.edit_message(tmp, 'Error: Parameter required.')
            return
        rand = random.randint(0, 9)
        (result, error) = googleimages.search(args[1], creds, rand)
        if error == 0:
            await client.edit_message(tmp, '{},\n{}'.format(message.author.mention, result))
        else:
            await client.edit_message(tmp, 'Error: {}'.format(result))

    elif message.content.startswith('-username'):
        if len(message.mentions) == 1:
            await client.send_message(message.channel, 'Username for specified user is: ``{}``.'.format(message.mentions[0].name))
        else:
            await client.send_message(message.channel, 'Error: You didn\'t specify a user, or specified too many.')

    elif message.content.startswith('-addquote'):
        tmp = await client.send_message(message.channel, 'Attempting to add quote...')
        args = message.content.split(' ')
        if len(args) < 2:
            await client.edit_message(tmp, 'Error: Parameter required.')
            return

        try:
            msg = await client.get_message(message.channel, args[1])
            quote = [msg.content]
            quote_author_id = msg.author.id
            quote_author = msg.author.name
            quote_id = msg.id
        except discord.NotFound:
            await client.edit_message(tmp, 'Error: The message with that ID could not be found.')
        except discord.Forbidden:
            await client.edit_message(tmp, 'Error: Was unable to get the message.')
        else:
            if len(args) > 2:
                if len(args) > 13:
                    await client.edit_message(tmp, 'Error: Too many messages for one quote.')
                    return
                quote_ids = [msg.id]
                for postid in args[2:]:
                    try:
                        tmp2 = await client.send_message(message.channel, 'Attempting to add secondary quotes...')
                        msg = await client.get_message(message.channel, postid)
                    except discord.NotFound:
                        await client.edit_message(tmp2, 'Error: The message with that ID could not be found. Skipping.')
                    except discord.Forbidden:
                        await client.edit_message(tmp2, 'Error: Was unable to get the message. Skipping.')
                    else:
                        if msg.author.id != quote_author_id:
                            await client.edit_message(tmp2, 'Error: The author of that message is not consistent with '
                                                            'the first message.')
                            await client.edit_message(tmp, 'Error: Inconsistent authors. Terminating.')
                            return
                        else:
                            await asyncio.sleep(1)
                            await client.delete_message(tmp2)
                            quote_ids.append(msg.id)
                            quote.append(msg.content)
                quote_ids.sort()
                string = "-".join(quote_ids)
                quote_id = md5(string.encode()).hexdigest()
        if quotes.add_quote("\n".join(quote), quote_author_id, quote_id) == 1:
            await client.edit_message(tmp, 'Successfully added quote #{} for {}.'.format(quote_id,quote_author))
        else:
            await client.edit_message(tmp, 'Failed to add quote for {}.'.format(quote_author))


    elif message.content.startswith('-quote'):
        tmp = await client.send_message(message.channel, 'Fetching quote...')
        args = message.content.split(' ', 1)
        if len(args) != 2:
            await client.edit_message(tmp, 'Error: Parameter required.')
            return
        member = discord.utils.find(lambda m: m.name == args[1], message.channel.server.members)
        if member is None:
            await client.edit_message(tmp, 'Error: Could not find any user called {}.'.format(args[1]))
            return
        (quote,_id) = quotes.get_quote(member.id)
        if quote is None:
            await client.edit_message(tmp, 'Error: Could not find any quotes for {}.'.format(member.name))
        else:
            await client.edit_message(tmp, '``#{}``:\n```{}```'.format(_id,quote))
    elif message.content.startswith('-delquote'):
        tmp = await client.send_message(message.channel, 'Attempting to delete quote...')
        args = message.content.split(' ', 1)
        if len(args) != 2:
            await client.edit_message(tmp, 'Error: Parameter required.')
            return
        if quotes.del_quote(args[1]) == 1:
            await client.edit_message(tmp, 'Successfully deleted quote #{}.'.format(args[1]))
        else:
            await client.edit_message(tmp, 'Failed to delete quote #{}.'.format(args[1]))
    elif message.content.startswith('-idquote'):
        tmp = await client.send_message(message.channel, 'Fetching quote...')
        args = message.content.split(' ', 1)
        if len(args) != 2:
            await client.edit_message(tmp, 'Error: Parameter required.')
            return
        (quote, id) = quotes.get_quote_id(args[1])
        if quote is None:
            await client.edit_message(tmp, 'Error: Could not find any quote with id #{}.'.format(args[1]))
        else:
            await client.edit_message(tmp, '``#{}``:\n```{}```'.format(id, quote))

    elif message.content.startswith('-sfwdanbooru'):
        await danbooru_search(message,method='sfw')
    elif message.content.startswith('-nsfwdanbooru'):
        await danbooru_search(message, method='nsfw')
    elif message.content.startswith('-danbooru'):
        await danbooru_search(message, method='other')
    elif message.content.startswith('-tagsearch'):
        tmp = await client.send_message(message.channel, 'Searching for tags...')
        args = message.content.split(' ', 1)
        (result, error) = danbooru.tagsearch(args[1])
        if error == 0:
            await client.edit_message(tmp, '{},\n{}'.format(message.author.mention, result))
        else:
            await client.edit_message(tmp, 'Error: {}'.format(result))

    elif message.content.startswith('-sfwgelbooru'):
        await gelbooru_search(message,method='sfw')
    elif message.content.startswith('-nsfwgelbooru'):
        await gelbooru_search(message, method='nsfw')
    elif message.content.startswith('-gelbooru'):
        await gelbooru_search(message, method='other')

    elif message.content.startswith('-nickname'):
        tmp = await client.send_message(message.channel, 'Changing nickname ~~')
        args = message.content.split(' ', 1)
        if len(args) != 2:
            await client.edit_message(tmp, 'Error: Incorrect number of parameters provided.')
            return
        me = message.server.get_member(client.user.id)
        await client.change_nickname(me,args[1])
        await client.edit_message(tmp, 'Changed nickname to {}'.format(args[1]))

    elif message.content.startswith('#refresh'):
        tmp = await client.send_message(message.channel, 'Updating to newest settings')
        fh = open('profile.png', 'rb')
        await client.edit_profile(username=creds['username'],avatar=fh.read())
        fh.close()
        await client.edit_message(tmp, 'Finished updating!')

    elif message.content.startswith('#ban'):
        tmp = await client.send_message(message.channel, 'Telling user to fuck off...')
        args = message.content.split(' ', 1)
        member = discord.utils.find(lambda m: m.name == args[1], message.channel.server.members)
        await client.ban(member)
        await client.edit_message(tmp, 'Fuck off {}.' .format(member.name))

async def danbooru_search (message, method):
    tmp = await client.send_message(message.channel, 'Searching for posts in Danbooru...')
    m = re.search(r'page=(\d+)', message.content)
    if m:
        message.content = re.sub(r'page=(\d+)', '', message.content)
        page = int(m.group(1))
    else:
        page = 0
    args = message.content.split(' ', 1)
    if len(args) != 2:
        await client.edit_message(tmp, 'Error: Incorrect number of parameters provided.')
        return
    else:
        (result, error) = danbooru.search(method=method, query=args[1], page=page)
        if error == 0:
            await client.edit_message(tmp, '{},\n{}'.format(message.author.mention, result))
        else:
            await client.edit_message(tmp, 'Error: {}'.format(result))

async def gelbooru_search (message, method):
    tmp = await client.send_message(message.channel, 'Searching for posts in Gelbooru...')
    m = re.search(r'page=(\d+)', message.content)
    if m:
        message.content = re.sub(r'page=(\d+)', '', message.content)
        page = int(m.group(1))
    else:
        page = 0
    args = message.content.split(' ', 1)
    if len(args) != 2:
        await client.edit_message(tmp, 'Error: Incorrect number of parameters provided.')
        return
    else:
        (result, error) = gelbooru.search(method=method, query=args[1], page=page)
        if error == 0:
            await client.edit_message(tmp, '{},\n{}'.format(message.author.mention, result))
        else:
            await client.edit_message(tmp, 'Error: {}'.format(result))


@client.event
async def on_member_update(before, after):
    global tell
    memos = []
    for _memo in tell:
        if _memo.to.id == after.id:
            memos.append(_memo)
    for memo in memos:
        if memo is not None:
            if after.server == memo.channel.server and after.status == discord.Status.online:
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
