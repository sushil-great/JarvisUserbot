import os
import sys

from jarvis import CMD_HNDLR, SUDO_HNDLR
from jarvis.utils import j_cmd, edit_or_reply, sudo_cmd


@jarvis.on(j_cmd(pattern="restart", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await edit_or_reply(event,f"Restarted. `{CMD_HNDLR}ping` or `{CMD_HNDLR}help` to check if I am online",)
    await jarvis.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()


@jarvis.on(sudo_cmd(pattern="restart", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await edit_or_reply(event,f"Restarted. `{SUDO_HNDLR}ping` or `{SUDO_HNDLR}help` to check if I am online",)
    await jarvis.disconnect()
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()


@jarvis.on(j_cmd(pattern="shutdown", outgoing=True))
@jarvis.on(sudo_cmd(pattern="shutdown", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    await edit_or_reply(event, "Turning off ...Manually turn me on later")
    await jarvis.disconnect()

@jarvis.on(j_cmd(pattern="upgrade", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await edit_or_reply(
        event,
        f"Updated. `{CMD_HNDLR}ping` or `{CMD_HNDLR}help` to check if I am online",
    )
    await jarvis.disconnect()
    os.system("git pull")
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()
