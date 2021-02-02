# Probot - A Multi Purpose Bot
# Copyright (C) 2020 -21 Sppidy
# AGPL License
# This file is a part of < https://github.com/sppidy/ProBot >
# Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.


from pyrogram.types import Message
from jarvis.bot.probot import bot
from jarvis.bot.plugins.admin import __doc__ as doc1
from jarvis.bot.plugins.misc import __doc__ as doc2
from jarvis.bot.plugins.devs import __doc__ as doc3
from jarvis.bot.plugins.channel import __doc__ as doc4
from jarvis.bot.plugins.essentials import __doc__ as doc5
from jarvis.bot import USERNAME
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery)

ADMIN_PIC = "https://i.imgur.com/2L55ZMh.png"
DEV_PIC = "https://i.imgur.com/qIROuGX.png"
MISC_PIC = "https://i.imgur.com/9Ko6GQx.png"
CHNL_PIC = "https://i.imgur.com/NqIzUjC.png"
ESN_PIC = "https://i.imgur.com/abySvWV.png"

@bot.on_inline_query()
def answer(client, inline_query):
    inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title="Help For Admin Plugin",
                description="Inline Help Menu For Admin Plugin",
                input_message_content=InputTextMessageContent(f"**Help Menu**\n\n**Note These Commands Will Work Only If** @{USERNAME} **Is There In Your Group**\n\n{doc1}"),
                thumb_url=ADMIN_PIC,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"Help Again !",switch_inline_query_current_chat="")]]),
            ),InlineQueryResultArticle(
                title="Help For Misc Module",
                description="Inline Help Menu For Misc Plugins",
                input_message_content=InputTextMessageContent(f"**Help On Misc Module**\n\n**Note These Commands Will Work Only If** @{USERNAME} **Is There In Your Group**\n\n{doc2}"),
                thumb_url=MISC_PIC,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"Help Again !",switch_inline_query_current_chat="")]]),
            ),InlineQueryResultArticle(
                title="Help For Devs Module",
                description="Inline Help Menu For Dev Commands",
                input_message_content=InputTextMessageContent(f"**Help On Dev Module**\n\n**Note These Commands Will Work Only If** @{USERNAME} **Is There In Your Group**\n\n{doc3}"),
                thumb_url=DEV_PIC,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"Help Again !",switch_inline_query_current_chat="")]]),
            ),InlineQueryResultArticle(
                title="Help For Channel Module",
                description="Inline Help Menu For Channel Module",
                input_message_content=InputTextMessageContent(f"**Help On Channel Module**\n\n**Note These Commands Will Work Only If** @{USERNAME} **Is There In Your Group**\n\n{doc4}"),
                thumb_url=CHNL_PIC,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"Help Again !",switch_inline_query_current_chat="")]]),
            ),InlineQueryResultArticle(
                title="Help For Essential Module",
                description="Inline Help Menu For Essential Module",
                input_message_content=InputTextMessageContent(f"**Help On Essential Module**\n\n**Note These Commands Will Work Only If** @{USERNAME} **Is There In Your Group**\n\n{doc5}"),
                thumb_url=ESN_PIC,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"Help Again !",switch_inline_query_current_chat="")]]),
            ),
        ],
        cache_time=1
    )
