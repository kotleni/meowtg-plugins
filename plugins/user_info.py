from plugin_base import PluginBase
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import SendReactionRequest
import subprocess

class UserInfo(PluginBase):
    def __init__(self, header, api) -> None:
        super().__init__(header, api)

    async def on_command(self, event, args) -> str:
        if args[0] == "user":
            output = f"{event.sender.first_name} ({event.sender.username})\n"
            output += f"{event.sender.id}\n"
            output += f"{event.sender.phone}"

            return output
