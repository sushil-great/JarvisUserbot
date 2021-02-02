# A Part of This File Is Taken From Spechide's Pyro Bot

# Edits and Converted to Markdown By @sppidy

"""
Plugin Name : Devs 
Commannds :- 
~  /bash 
    Function :- Executes Linux Commands
~ /run -
    Function =  Runs or Evaluvates Python Code
~ /restart -
    Function = Restart Thes Bot (Works Only If Hosted On VPS) 
~ /upgrade - 
    Function = Upgrades The Bot to Latest Code in Github (Works Only If Hosted On VPS)

Note These are owner Restricted Commands

"""
import io
import sys
import traceback
import asyncio
import os
import html
import re
import traceback
from contextlib import redirect_stdout
from pyrogram import Client, filters
from jarvis.bot.probot import bot
from jarvis.bot import OWNER
from jarvis.bot import USERNAME as UN 

@bot.on_message(filters.regex("^/run") & filters.user(f"{OWNER}") & ~filters.edited)
async def eval(client, message):
    status_message = await message.reply_text(".....")
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"

    final_output = "**RUN**: "
    final_output += f"`{cmd}`\n\n"
    final_output += "**OUTPUT**:\n"
    final_output += f"`{evaluation.strip()}` \n"

    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "run.txt"
            await reply_to_.reply_document(
                document=out_file,
                caption=cmd,
                disable_notification=True
            )
    else:
        await reply_to_.reply_text(final_output)
    await status_message.delete()


async def aexec(code, client, message):
    exec(
        'async def __aexec(client, message): ' +
        ''.join(f'\n {l_}' for l_ in code.split('\n'))
    )
    return await locals()['__aexec'](client, message)
    
@bot.on_message(filters.regex("^/bash") & filters.user(f"{OWNER}") & ~filters.edited)
async def execution(_, message):
    status_message = await message.reply_text(".....")
    # DELAY_BETWEEN_EDITS = 0.3
    # PROCESS_RUN_TIME = 100
    cmd = message.text.split(" ", maxsplit=1)[1]

    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message

    # start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    e = stderr.decode()
    if not e:
        e = "No Error"
    o = stdout.decode()
    if not o:
        o = "No Output"

    OUTPUT = ""
    OUTPUT += f"__QUERY:__\n**Command:**\n`{cmd}`\n\n"
    OUTPUT += f"__PID__: `{process.pid}`\n\n"
    OUTPUT += f"__ERRORS__: \n`{e}`\n\n"
    OUTPUT += f"__OUTPUT__: \n`{o}`"

    if len(OUTPUT) > 4096:
        with BytesIO(str.encode(OUTPUT)) as out_file:
            out_file.name = "bash.txt"
            await reply_to_.reply_document(
                document=out_file,
                caption=cmd,
                disable_notification=True
            )
    else:
        await reply_to_.reply_text(OUTPUT)

    await status_message.delete()

@bot.on_message(filters.command(["upgrade",f"upgrade@{UN}"]) & filters.user(f"{OWNER}") & ~filters.edited)
async def upgrade(client, message):
    sm = await message.reply_text("Upgrading sources...")
    proc = await asyncio.create_subprocess_shell("git pull --no-edit",
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.STDOUT)
    stdout = (await proc.communicate())[0]
    if proc.returncode == 0:
        if "Already up to date." in stdout.decode():
            await sm.edit_text("There's nothing to upgrade.")
        else:
            await sm.edit_text("Restarting")
            os.execl(sys.executable, sys.executable, *sys.argv)  # skipcq: BAN-B606
    else:
        await sm.edit_text(f"Upgrade failed (process exited with {proc.returncode}):\n{stdout.decode()}")
        proc = await asyncio.create_subprocess_shell("git merge --abort")
        await proc.communicate()

@bot.on_message(filters.command(["restart",f"restart@{UN}"]) & filters.user(f"{OWNER}") & ~filters.edited)
async def restart(client, message):
    await message.reply_text("Restarting Pls Wait")
    os.execl(sys.executable, sys.executable, *sys.argv)
