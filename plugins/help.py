from plugin_base import PluginBase
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import SendReactionRequest

class Help(PluginBase):
    def __init__(self, header, api) -> None:
        super().__init__(header, api)
    
    async def load(self):
        pass

    async def on_command(self, event, args) -> str:
        if args[0] == "plugins":
            output = ""
            for plugin in self.api.plugins_loader.plugins:
                class_name = plugin.__class__.__name__
                description = plugin.description
                if plugin.__doc__:
                    description = plugin.__doc__

                output += f'{class_name} - {description}\n'
                
            return output
