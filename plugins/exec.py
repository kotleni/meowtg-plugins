from plugin_base import PluginBase
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import SendReactionRequest

class Exec(PluginBase):
    """Execute python script <code>"""
    
    enabled = True
    
    def __init__(self, api) -> None:
        super().__init__(api)
    
    async def load(self):
        pass

    async def on_command(self, event, args) -> str:
        if args[0] == "exec":
            result = ''
            try:
                message_text = event.text
                code = message_text.replace('.exec', '').('```', '')
                result = exec(code)
            except Exception as e:
                result = e
            return result
