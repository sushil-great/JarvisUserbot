# Probot - A Multi Purpose Bot
# Copyright (C) 2020 -21 Sppidy
# AGPL License
# This file is a part of < https://github.com/sppidy/ProBot >
# Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

from bot import version, botname
from bot import USERNAME as UN
from pyrogram import filters
from jarvis.bot.probot import bot
from pyrogram.types import Message
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardButton)
  
@bot.on_message(filters.regex("^/help") & (filters.private) & ~(filters.edited))
async def helppmstart(bot, message):
  client = message._client
  chat_id=message.chat.id
  await bot.send_message(chat_id=chat_id,text="**Click the Button For Help**",
                            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(f"Click Here For Help !",switch_inline_query_current_chat="")]]),
                           )
  
@bot.on_message(filters.regex("^/help") & (filters.group) & ~(filters.edited))
async def helpgrpstart(bot, message):
  client = message._client
  chat_id=message.chat.id
  boot = await client.get_me()
  URL = "t.me/" + f"{boot.username}?start=help"
  await bot.send_message(chat_id=chat_id,
                         reply_to_message_id=message.message_id,
                         text="Contact Me In Pm For Help")
