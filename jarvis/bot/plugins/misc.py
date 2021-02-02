# Probot - A Multi Purpose Bot
# Copyright (C) 2020 -21 Sppidy
# AGPL License
# This file is a part of < https://github.com/sppidy/ProBot >
# Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

"""
Plugin Name : Misc

Commannds :- 
~ /echo 
    Example :- /echo hi
~ /paste -
    Function = Pastes in Deldog
    Example :- /paste Reply A Message/Give Text 
~ /haste -
    Function = Pastes in hastebin
    Example :- /haste Reply A Message/Give Text 
~ /whois -
    Function = Give The User's Info
    Example :- /whois @username
~ /ping - 
    Function = Checks Bot's Speed
~ /ip - 
    Function = Fetches Info Of a Website or Ip Address
    Example :- /ip google.com
~ /sid - 
    Function = Give Sticker ID of Replied Sticker
    Example :- /sid (Repling a Sticker)
~ /json - 
    Function = Fetches Detailed Info amessage
    Example :- /json (Repling a Message)
~ /source - 
    Function = Gives the bot's Source page

Will Add More Plugins Soon
"""

import os
import re
import time
import requests
from pyrogram import Client, filters
from jarvis.bot.probot import bot
from pyrogram.types import Message
from datetime import datetime
from pyrogram.types import User
from pyrogram.raw import functions
from pyrogram.errors import PeerIdInvalid
from aiohttp import ClientSession
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardButton)
from bot import USERNAME as UN
@bot.on_message(filters.regex('^/echo (?P<text>.+)') & ~filters.edited)
async def on_echo(client, message):
    text = message.matches[0]['text']
    
    if message.reply_to_message:
        return await message.reply_to_message.reply(text, quote=True)
    await message.reply(text)

# Thanks to @New-dev0 For This Plugin

@bot.on_message(filters.command(["paste",f"paste@{UN}"]) & ~filters.edited)
async def dogbin(client, message):
    if message.reply_to_message:
        if message.reply_to_message.document:
            tfile = message.reply_to_message
            to_file = await tfile.download()
            m_list = None
            with open(to_file,'rb') as fd:
                m_list = fd.readlines()
            mean=""
            for s in m_list:
                mean+= s.decode('UTF-8') +"\r\n"
            url = f"https://del.dog/documents"
            r = requests.post(url,data = mean.encode('UTF-8')).json()
            url = f"https://del.dog/{r['key']}"
            await message.reply_text(f"Pasted [Here]({url})",disable_web_page_preview=True)
        if message.reply_to_message.text:
            mean = message.reply_to_message.text
            url = f"https://del.dog/documents"
            r = requests.post(url,data = mean.encode('UTF-8')).json()
            url = f"https://del.dog/{r['key']}"
            await message.reply_text(f"Pasted [Here]({url})",disable_web_page_preview=True)
    else:
        await message.reply_text("Please Reply to text or document.")
        

@bot.on_message(filters.command(commands=["ping",f"ping@{UN}"]) & ~filters.edited)
async def ping(_, message: Message):
    start = datetime.now()
    event = await message.reply_text("...")
    end = datetime.now()
    ms = (end-start).microseconds / 1000
    await event.edit(f"**Pong** !!\n{ms} ms ")
    

def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id

infotext = (
    " * **[{full_name}](tg://user?id={user_id})**\n"
    " * UserID: `{user_id}`\n"
    " * First Name: `{first_name}`\n"
    " * Last Name: `{last_name}`\n"
    " * Username: `{username}`\n"
    " * Last Online: `{last_online}`\n"
    " * Bio: {bio}")

def LastOnline(user: User):
    if user.is_bot:
        return ""
    elif user.status == 'recently':
        return "Recently"
    elif user.status == 'within_week':
        return "Within the last week"
    elif user.status == 'within_month':
        return "Within the last month"
    elif user.status == 'long_time_ago':
        return "A long time ago :("
    elif user.status == 'online':
        return "Currently Online"
    elif user.status == 'offline':
        return datetime.fromtimestamp(user.status.date).strftime("%a, %d %b %Y, %H:%M:%S")


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name

@bot.on_message(filters.command(['whois',f"whois@{UN}"]) & ~filters.edited)
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("I don't know that User.")
        return
    desc = await client.get_chat(get_user)
    desc = desc.description
    await message.reply_text(
            infotext.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                bio=desc if desc else "`No bio set up.`"),
            disable_web_page_preview=True)


@bot.on_message(filters.regex("^/ip (?P<text>.+)") & ~filters.edited)
async def ip(client, m: Message):
    ip = m.matches[0]['text']

    aioclient = ClientSession()
    if not ip:
        await m.reply_text("Provide an IP!")
        return

    async with aioclient.get(f"http://ip-api.com/json/{ip}") as response:
        if response.status == 200:
            lookup_json = await response.json()
        else:
            await m.reply_text(f"An error occurred when looking for {ip}: {response.status}")
            return

    fixed_lookup = {}

    for key, value in lookup_json.items():
        special = {"lat": "Latitude", "lon": "Longitude",
                   "isp": "ISP", "as": "AS", "asname": "AS name"}
        if key in special:
            fixed_lookup[special[key]] = str(value)
            continue

        key = re.sub(r"([a-z])([A-Z])", r"\g<1> \g<2>", key)
        key = key.capitalize()

        if not value:
            value = "None"

        fixed_lookup[key] = str(value)

    text = ""

    for key, value in fixed_lookup.items():
        text = text + f"**{key}:** {value}\n"

    await m.reply_text(text, parse_mode="markdown")
    

@bot.on_message(filters.command(['sid',f"sid@{UN}"]) & filters.reply & ~filters.edited)
async def stickerid(client,message):
    if message.reply_to_message.sticker:
        await message.reply_text(f"**Sticker ID** :- `{message.reply_to_message.sticker.file_id}`",quote=True)
    else:
        await message.reply_text('Reply to a sticker')

@bot.on_message(filters.command(["json",f"json@{UN}"]))
async def jsonify(_, message):
    pronub = None
    reply_to_id = None

    if message.reply_to_message:
        pronub = message.reply_to_message
    else:
        pronub = message

    try:
        await message.reply_text(f"`{pronub}`")
    except Exception as e:
        with open("json.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(pronub))
        await message.reply_document(
            document="json.text",
            caption=str(e),
            disable_notification=True,
            reply_to_message_id=reply_to_id
        )
        os.remove("json.text")
        
@bot.on_message(filters.command(["haste",f"haste@{UN}"]) & ~filters.edited)
async def hastebin(client, message):
    if message.reply_to_message:
        if message.reply_to_message.document:
            tfile = message.reply_to_message
            to_file = await tfile.download()
            m_list = None
            with open(to_file,'rb') as fd:
                m_list = fd.readlines()
            mean=""
            for s in m_list:
                mean+= s.decode('UTF-8') +"\r\n"
            url = f"https://hastebin.com/documents"
            r = requests.post(url,data = mean.encode('UTF-8')).json()
            url = f"https://hastebin.com/{r['key']}"
            await message.reply_text(f"Pasted Below",reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Click Here", url=f"{url}")]]),disable_web_page_preview=True)
        if message.reply_to_message.text:
            mean = message.reply_to_message.text
            url = f"https://hastebin.com/documents"
            r = requests.post(url,data = mean.encode('UTF-8')).json()
            url = f"https://hastebin.com/{r['key']}"
            await message.reply_text(f"Pasted Below",reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Click Here", url=f"{url}")]]),disable_web_page_preview=True)
    else:
        await message.reply_text("Please Reply to text or document.")

@bot.on_message(filters.command(["source",f"source@{UN}"]) & ~filters.edited)
async def source(c:bot,m:Message):
    await m.reply_text("https://github.com/Jarvis-Works/JarvisUserbot\n**Star The Repo if U like**", disable_web_page_preview=True)
