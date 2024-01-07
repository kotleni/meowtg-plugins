from plugin_base import PluginBase
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import SendReactionRequest
import subprocess
# by awlik 07.01.2024

class CommandLineExecutor:
    """Stolen from cmd.py"""
    def execute(self, command):
        return subprocess.run(command, shell=True, capture_output=True)


class CompilerC(PluginBase):
    """Show c code: .c <code> or .c <reply>"""

    enabled = True

    executor = CommandLineExecutor()

    def __init__(self, api) -> None:
        super().__init__(api)

    async def on_command(self, event, args) -> str:
        if args[0] == "c":
            chat = await event.get_chat()
            message = event.message
            if event.reply_to:
                message = await self.api.client.get_messages(chat.id, ids=event.reply_to.reply_to_msg_id)

            with open('temp.c', 'w') as file:
                file.write(message.text.replace('.c', '').replace('```', '')

            output = self.executor.execute('gcc temp.c -o temp.o').stderr.decode('utf-8')
            output += str(self.executor.execute('./temp.o').stdout.decode('utf-8'))
            
            return output
