# Probot - A Multi Purpose Bot
# Copyright (C) 2020 -21 Sppidy
# AGPL License
# This file is a part of < https://github.com/sppidy/ProBot >
# Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

botname = "Jarvis Assistant"
version = 0.2
copyright = "(C) Copyright  2020-21 Spidy <https://github.com/sppidy>"
license = "Licensed Under GNU AFFERO GENERAL PUBLIC LICENSE (AGPL - 3.0)"


from pyrogram import Client
from jarvis.bot.var import vars
from pyrogram.errors.exceptions.bad_request_400 import BadRequest
import logging
logging.basicConfig(
    level=logging.INFO,
    format=' ✘ %(levelname)s • %(message)s'
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

LOGGER = logging.getLogger(__name__)
APP_ID = vars.APP_ID
API_HASH = vars.API_HASH
BOT_TOKEN = vars.BOT_TOKEN
OWNER = vars.OWNER
