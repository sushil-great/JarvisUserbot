# SomePart of This File is Taken From Spechide's Pyrobot
# Some Mods by Sppidy

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.types import ChatPermissions
from googletrans import LANGUAGES

async def admin_check(message: Message) -> bool:
    if not message.from_user:
        return False
    if message.chat.type not in ["supergroup", "channel"]:
        return False
    if message.from_user.id in [
        777000,  # Telegram Service Notifications
        1087968824  # GroupAnonymousBot
    ]:
        return True
    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id
    check_status = await client.get_chat_member(
        chat_id=chat_id,
        user_id=user_id
    )
    admin_strings = [
        "creator",
        "administrator"
    ]
    # https://git.colinshark.de/PyroBot/PyroBot/src/branch/master/pyrobot/modules/admin.py#L69
    if check_status.status not in admin_strings:
        return False
    else:
        return True

async def adminofilter(filt, client, message):
    return await admin_check(message)

def extract_user(message: Message) -> (int, str):
    """extracts the user from a message"""
    user_id = None
    user_first_name = None

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        user_first_name = message.reply_to_message.from_user.first_name

    elif len(message.command) > 1:
        if len(message.entities) > 1:
            # 0: is the command used
            # 1: should be the user specified
            required_entity = message.entities[1]
            if required_entity.type == "text_mention":
                user_id = required_entity.user.id
                user_first_name = required_entity.user.first_name
            elif required_entity.type == "mention":
                user_id = message.text[
                    required_entity.offset:
                    required_entity.offset + required_entity.length
                ]
                # don't want to make a request -_-
                user_first_name = user_id
        else:
            user_id = message.command[1]
            # don't want to make a request -_-
            user_first_name = user_id

    else:
        user_id = message.from_user.id
        user_first_name = message.from_user.first_name

    return (user_id, user_first_name)


admin_fliter = filters.create(
    func=adminofilter,
    name="adminfilter"
)

def get_tr_lang(text):
    if len(text.split()) > 0:
        lang = text.split()[0]
        if lang.split("-")[0] not in LANGUAGES:
            lang = "en"
        if len(lang.split("-")) > 1:
            if lang.split("-")[1] not in LANGUAGES:
                lang = "en"
    else:
        lang = "en"
    return lang
