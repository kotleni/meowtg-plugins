from plugin_base import PluginBase
from telethon import TelegramClient, events, types, functions
from telethon.tl.functions.messages import SendReactionRequest
import subprocess
#by awlik 09.01.2024
class UserInfo:
  def __init__(who):
    self.first_name = who.first_name
    self.last_name = who.last_name
    self.id = who.user_id
    self.avatar = who.avatar
  
class AdvancedUserInfo(PluginBase):
    """Andvanced User info by .userinfo command"""
    enabled = True

    def __init__(self, api) -> None:
        super().__init__(api)
        
    async def on_command(self, event, args) -> str:
        if args[0] == "userinfo":
          if len(args) == 1:
            output = f"{event.chat.first_name} ({event.chat.username})\n"
            output += f"{event.chat.id}\n"
            output += f"{event.chat.phone}"

            return output
