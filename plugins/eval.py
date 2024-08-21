from plugin_base import PluginBase
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import SendReactionRequest

class Eval(PluginBase):
    def __init__(self, header, api) -> None:
        super().__init__(header, api)
    
    async def load(self):
        pass

    async def on_command(self, event, args) -> str:
        if args[0] == "eval":
            result = ''
            try:
                message_text = event.text
                code = message_text[6:]
                result = eval(code)
            except Exception as e:
                result = e
            return str(result)
