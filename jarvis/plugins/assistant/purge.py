from telethon import events, custom, Button
from telethon.tl.types import (
    Channel,
    Chat,
    User
)

import emoji
from googletrans import Translator
from jarvis.utils import admin_cmd, edit_or_reply, sudo_cmd
from telethon.utils import get_display_name
from jarvis.utils import admin_cmd, sudo_cmd
from jarvis.uniborgConfig import Config
from telethon import events
from datetime import datetime
from jarvis.utils import admin_cmd, edit_or_reply, sudo_cmd
import time
from jarvis import Lastupdate, bot
import asyncio
from jarvis.utils import bot
from telethon import events
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.tl.types import ChannelParticipantsAdmins

from asyncio import sleep
from os import remove

from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
    UserAdminInvalidError,
)
from telethon.errors.rpcerrorlist import MessageTooLongError, UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)

from jarvis import BOTLOG, BOTLOG_CHATID, CMD_HELP
from jarvis.utils import admin_cmd, errors_handler, register, sudo_cmd
OWNER_ID = bot.uid
# Check if user has admin rights
async def is_administrator(user_id: int, message):
    admin = False
    async for user in tgbot.iter_participants(message.chat_id,
                             filter=ChannelParticipantsAdmins):
        if user_id == user.id or OWNER_ID :
            admin = True
            break
    return admin


@tgbot.on(events.NewMessage(pattern='^/purge'))
async def purge(event):
        chat = event.chat_id
        msgs = []

        if not await is_administrator(user_id=event.from_id, message=event):
           await event.reply("You're not an admin!")
           return

        msg = await event.get_reply_message()
        if not msg:
           await event.reply("Reply to a message to select where to start purging from.")
           return

        try:
           msg_id = msg.id
           count = 0        
           to_delete = event.message.id - 1
           await event.tgbot.delete_messages(chat, event.message.id)
           msgs.append(event.reply_to_msg_id)
           for m_id in range(to_delete, msg_id - 1, -1):
               msgs.append(m_id)
               count += 1            
               if len(msgs) == 100:
                   await event.tgbot.delete_messages(chat, msgs)
                   msgs = []

           await event.tgbot.delete_messages(chat, msgs)
           del_res = await event.tgbot.send_message(
           event.chat_id, f"Fast Purged {count} messages.")

           await asyncio.sleep(4)
           await del_res.delete()

        except MessageDeleteForbiddenError:
            text = "Failed to delete messages.\n"
            text += "Messages maybe too old or I'm not admin! or dont have delete rights!"
            del_res = await event.respond(text, parse_mode='md')
            await asyncio.sleep(5)
            await del_res.delete()


@tgbot.on(events.NewMessage(pattern="^/del$"))
async def delete_msg(event):

    if not await is_administrator(user_id=event.from_id, message=event):
        await event.reply("You're not an admin!")
        return

    chat = event.chat_id
    msg = await event.get_reply_message()
    if not msg:
        await event.reply("Reply to some message to delete it.")
        return
    to_delete = event.message
    chat = await event.get_input_chat()
    rm = [msg, to_delete]
    await event.tgbot.delete_messages(chat, rm)