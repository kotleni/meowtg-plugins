from plugin_base import PluginBase
from telethon import TelegramClient, events, types, functions
from telethon.tl.functions.messages import SendReactionRequest
import subprocess
#by awlik 09.01.2024
class UserInfo:
  def __init__(self, who, get_user=None, username=False):
    if get_user:
      who = who.client(functions.help.GetUserInfoRequest(user_id=username))
  
    self.first_name = who.first_name
    self.last_name = who.last_name
    self.id = who.from_id
    self.avatar = who.avatar

  
class AdvancedUserInfo(PluginBase):
    """Andvanced User info by .userinfo command"""
    enabled = True
    chat = event.get_chat()
    def __init__(self, api) -> None:
        super().__init__(api)
        
    async def on_command(self, event, args) -> str:
        if args[0] == "userinfo":
          if event.reply_to:
            message = await self.api.client.get_messages(chat.id, ids=event.reply_to.reply_to_msg_id)
            user = UserInfo(message, get_user=True)
          elif len(args) > 1:
            user = UserInfo(event, get_user=True, username=args[1])
          else:
            message = await self.api.client.get_messages(chat.id, ids=event.from_id)
            user = UserInfo(message)


           
        return f'Fist name: {user.first_name}\nLast name: {user.last_name}\nID: {user.id}\n'
