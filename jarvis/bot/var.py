# Probot - A Multi Purpose Bot
# Copyright (C) 2020 -21 Sppidy
# AGPL License
# This file is a part of < https://github.com/sppidy/ProBot >
# Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

import os
from dotenv import load_dotenv, find_dotenv
import var
from jarvis.bot.probot import bot

load_dotenv(find_dotenv())


class vars:
    BOT_TOKEN = os.getenv("TG_BOT_TOKEN")  # from @botfather
    APP_ID = os.getenv("APP_ID")  # from https://my.telegram.org/apps
    API_HASH = os.getenv("API_HASH")  # from https://my.telegram.org/apps
    OWNER = os.getenv("OWNER_ID") #Enter Your UserName Without @ For Some Special Funtionalities
    USERNAME = f"@{usrname.username}"
