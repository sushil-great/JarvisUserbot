# Probot - A Multi Purpose Bot
# Copyright (C) 2020 -21 Sppidy
# AGPL License
# This file is a part of < https://github.com/sppidy/ProBot >
# Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

"""
Plugin Name : Essentials
Commands :- 

~ /tr <Language Code> 
  Function :- Translates A Message to Your Desired Language
  
Will Add More Commands Soon
"""

# This Plugin Ported From EduuRobot

import html
from googletrans import Translator, LANGUAGES
from pyrogram import Client, filters
from pyrogram.types import Message
from jarvis.bot.helper import get_tr_lang
from jarvis.bot.probot import bot

translator = Translator()

@bot.on_message(filters.regex("^/tr") & ~filters.edited)
async def translate(c: Client, m: Message):
    text = m.text[4:]
    lang = get_tr_lang(text)
    text = text.replace(lang, "", 1).strip() if text.startswith(lang) else text
    if m.reply_to_message and not text:
        text = m.reply_to_message.text or m.reply_to_message.caption

    if not text:
        return await m.reply_text("translate_usage",
                                  reply_to_message_id=m.message_id)

    reply_to = m.reply_to_message or m
    sent = await m.reply_text("Translating..",reply_to_message_id=reply_to.message_id)
    langs = {}

    if len(lang.split("-")) > 1:
        langs["src"] = lang.split("-")[0]
        langs["dest"] = lang.split("-")[1]
    else:
        langs["dest"] = lang

    trres = translator.translate(text, **langs)
    text = trres.text

    await sent.edit_text(text, parse_mode=None)
