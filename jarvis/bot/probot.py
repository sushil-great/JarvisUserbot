# Probot - A Multi Purpose Bot
# Copyright (C) 2020 -21 Sppidy
# AGPL License
# This file is a part of < https://github.com/sppidy/ProBot >
# Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

from pyrogram import Client, idle
from bot.var import vars
from pyrogram import __version__
from pyrogram.raw.all import layer
from bot import botname, copyright, version, license, LOGGER

APP_ID = vars.APP_ID
API_HASH = vars.API_HASH
BOT_TOKEN = vars.BOT_TOKEN
TMP_DIR = "./downloads"


class bot(Client):

    def __init__(self):
        name = self.__class__.__name__.lower()

        
        super().__init__(
                ":memory:",
                plugins=dict(root="jarvis/bot/plugins"),
                workdir=TMP_DIR,
                api_id=APP_ID,
                api_hash=API_HASH,
                bot_token=BOT_TOKEN
        )
        

    async def start(self):
        await super().start()

        usrname = await self.get_me()
        LOGGER.info(
            f"Probot based on Pyrogram v{__version__} \n"
            f"(Layer {layer}) started on @{usrname.username}.\n"
            f"{copyright}\n"
            f"{license}\n"
            f"Jarvis Assistant V{version} Has been Installed Successfully."
        )

    async def stop(self, *args):
        await super().stop()
        LOGGER.info("Jarvis Assistant stopped. Bye.")
