# Probot - A Multi Purpose Bot
# Copyright (C) 2020 -21 Sppidy
# AGPL License
# This file is a part of < https://github.com/sppidy/ProBot >
# Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

"""
Plugin Name : Admin
Commannds :- 
~ /pin 
    Function :- Pins the Replied Message in a Group
~ /mute -
    Function =  Mutes a Person in a Chat
~ /unmute -
    Function = Unmutes a Person In a Chat 
~ /purge - 
    Function = Delete All Message From The Replied Message
~ /del -
    Function = Deletes The Replied Mesaage
~ /ban -
    Function = Bans The Replied user
~ /unban -
    Function = UnBans The Mentioned user
    Example = /unban @anonymoushackker or /unban 817298629
~ /promote -
    Function = Promotes the Replied User
~ /demote -
    Function = Demotes the Replied User

Will Add More Commands Soon
"""



import asyncio
from pyrogram import filters,Client
from pyrogram.types import Message, ChatMember, ChatPermissions
from jarvis.plugins.bot.probot import bot
from jarvis.plugins.bot.helper import adminofilter, extract_user, admin_check
from jarvis.plugins.bot import USERNAME as UN
admin_fliter = filters.create(
    func=adminofilter,
    name="adminfilter"
)

@bot.on_message(filters.command(commands=["pin",f"pin@{UN}"]) & (filters.group) & admin_fliter & ~filters.edited)
async def pinmessage(client, message):
    await message.delete()
    await asyncio.sleep(0.2)
    await message.reply_to_message.pin()
    
@bot.on_message(filters.command(commands=["mute",f"mute@{UN}"]) & (filters.group) & admin_fliter & ~filters.edited)
async def mutemember(client, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            )
        )
        client = message._client
        chat_id = message.chat.id
        mention = f"[{user_first_name}](tg://user?id={user_id})"
        await client.send_message(
            chat_id=chat_id,
            text=f"**#Muted\n Muted {mention} Be Quiet Now !!!!**")
    except Exception as error:
        await message.reply_text(
            str(error)
        )


@bot.on_message(filters.command(commands=["unmute",f"unmute@{UN}"]) & (filters.group) & admin_fliter & ~filters.edited)
async def un_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.unban_member(
            user_id=user_id
        )
        mention = f"[{user_first_name}](tg://user?id={user_id})"
        client = message._client
        chat_id = message.chat.id
        await client.send_message(
        chat_id=chat_id,
        text=f"#Unmuted\n{mention} can Again Speak Now !!")
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    
@bot.on_message(filters.command(commands=["purge",f"purge@{UN}"]) & (filters.group) & admin_fliter & ~filters.edited)
async def purge(client, message):
    """ purge upto the replied message """
    if message.chat.type not in (("supergroup", "channel")):
        return

    is_admin = await admin_check(message)

    if not is_admin:
        return

    status_message = await message.reply_text("...", quote=True)
    await message.delete()
    message_ids = []
    count_del_etion_s = 0

    if message.reply_to_message:
        for a_s_message_id in range(
            message.reply_to_message.message_id,
            message.message_id
        ):
            
            message_ids.append(a_s_message_id)
            if len(message_ids) == 100:
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=message_ids,
                    revoke=True
                )
                count_del_etion_s += len(message_ids)
                message_ids = []
        if len(message_ids) > 0:
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message_ids,
                revoke=True
            )

    await status_message.edit_text(
        f"**Purged Successfully**"
    )
    await asyncio.sleep(5)
    await status_message.delete()
    
@bot.on_message(filters.command(commands=["del",f"del@{UN}"]) & (filters.group) & admin_fliter & ~filters.edited)
async def delmsg(client, message):
    await message.delete()
    await asyncio.sleep(0.2)
    await message.reply_to_message.delete()
   

@bot.on_message(filters.command(["ban",f"ban@{UN}"]) & filters.group & ~filters.edited)  
async def purge(c:bot,m:Message):
    hmm = m.from_user.id
    getmem = await m.chat.get_member(hmm)
    if getmem.status=="creator" or getmem.status=="administrator":
        if getmem.can_restrict_members==True or getmem.status=="creator":
            if m.reply_to_message:
                bot = await c.get_me()
                variable = await m.chat.get_member(bot.id)
                if m.reply_to_message.from_user.id != bot.id:
                    if variable.status=="administrator":
                        if variable.can_restrict_members==True:
                            replied_user = m.reply_to_message.from_user.id
                            get_ruser = await m.chat.get_member(replied_user)
                            if get_ruser.status=="creator" or "administrator":
                                try:
                                    await m.chat.kick_member(m.reply_to_message.from_user.id)
                                    await m.reply_text(f"{m.reply_to_message.from_user.mention} Banned")
                                except Exception as e:
                                    await m.reply_text(f"I cant ban that user \n",)
                            else:
                                await m.chat.kick_member(m.reply_to_message.from_user.id)
                                await m.reply_text(f"{m.reply_to_message.from_user.mention} Bannned")      
                        else:
                            await m.reply_text("Give me Right of Banning Members...")
                    else:
                        await m.reply_text("I am Not Admin in this Chat")
                else:
                    await m.reply_text("I am not going to Ban myself")
            else:
                await m.reply_text("Reply to a message")
        else:
            await m.reply_text("You are missing right of `Banning members`")
    else:
        await m.reply_text("Only Admins Can use this Commands !")
@bot.on_message(filters.command(["unban",f"fban@{UN}"]) & filters.group & ~filters.edited & admin_fliter)
async def un_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    user_id, user_first_name = extract_user(message)

    try:
        await message.chat.unban_member(
            user_id=user_id
        )
        mention = f"[{user_first_name}](tg://user?id={user_id})"
        client = message._client
        chat_id = message.chat.id
        await client.send_message(
        chat_id=chat_id,
        text=f"{mention} can Again Join Now !!")
    except Exception as error:
        await message.reply_text(
            str(error)
        )

@bot.on_message(filters.command(["promote",f"promote@{UN}"]) & ~filters.edited & filters.group)  
async def purge(c:bot,m:Message):
    hmm = m.from_user.id
    getmem = await m.chat.get_member(hmm)
    if getmem.status=="creator" or getmem.status=="administrator":
        if getmem.can_promote_members==True or getmem.status=="creator":
            if m.reply_to_message:
                bot = await c.get_me()
                variable = await m.chat.get_member(bot.id)
                if variable.status=="administrator":
                    if variable.can_promote_members==True:
                        replied_user = m.reply_to_message.from_user.id
                        get_ruser = await m.chat.get_member(replied_user)
                        if get_ruser.status != "creator" or "administrator":
                            await m.chat.promote_member(m.reply_to_message.from_user.id)
                            await m.reply_text(f"{m.reply_to_message.from_user.mention} **Promoted Successfully !**")  
                        else:
                            await m.reply_text(f"Replied user is Already a {get_ruser.status}")
                    else:
                        await m.reply_text("I Dont have right of **Add Admins**..")
                else:
                    await m.reply_text("I am Not Admin in this Chat")
            else:
                await m.reply_text("Reply to a Message")
        else:
            await m.reply_text("You are missing right of **Promoting/Demoting Members**")
    else:
        await m.reply_text("Only Admins Can use this Commands !")


@bot.on_message(filters.command(["demote",f"demote@{UN}"]) & filters.group & ~filters.edited)
async def purge(a:bot ,m:Message):
    hmm = m.from_user.id
    getmem = await m.chat.get_member(hmm)
    if getmem.status=="creator" or getmem.status=="administrator":
        if getmem.can_promote_members==True or getmem.status=="creator":
            if m.reply_to_message:
                bot = await a.get_me()
                variable = await m.chat.get_member(bot.id)
                if variable.status=="administrator":
                    if variable.can_promote_members==True:
                        replied_user = m.reply_to_message.from_user.id
                        get_ruser = await m.chat.get_member(replied_user)
                        if get_ruser.status != "creator" or "administrator":
                            await a.promote_chat_member(m.chat.id, m.reply_to_message.from_user.id,
                                                 can_change_info=False,
                                                 can_delete_messages=False,
                                                 can_restrict_members=False,
                                                 can_invite_users=False,
                                                 can_pin_messages=False)
                            await m.reply_text(f"{m.reply_to_message.from_user.mention} Demoted , Better Luck Next Time !")  
                        else:
                            await m.reply_text(f"Replied user is Already a {get_ruser.status}")
                    else:
                        await m.reply_text("I Dont have right of Add Admins..")
                else:
                    await m.reply_text("I am Not Admin in this Chat")
            else:
                await m.reply_text("Reply to a Message")
        else:
            await m.reply_text("You are missing right of Promoting/Demoting Members")
    else:
        await m.reply_text("Only Admins Can use this Commands !")