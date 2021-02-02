# Probot - A Multi Purpose Bot
# Copyright (C) 2020 -21 Sppidy @New-Dev0
# AGPL License
# This file is a part of < https://github.com/sppidy/ProBot >
# Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

"""
Plugin Name : Channel Manager
Commands :- 
~ /purge 
  Function :- Deletes all Message from the Replied Message in a Channel

Will Add More Commands Soon
"""
from pyrogram import filters
from jarvis.plugins.bot.probot import bot

@bot.on_message(filters.command('purge') & (filters.channel) & ~filters.edited)
async def tryit(client,message):
    cl=message._client
    getre = message.reply_to_message.message_id
    op = message.message_id
    takeit = range (getre,op+1)
    await cl.delete_messages(message.chat.id,takeit)
    
