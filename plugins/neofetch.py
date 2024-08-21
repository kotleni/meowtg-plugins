from plugin_base import PluginBase
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import SendReactionRequest
import subprocess
import re
import platform

class CommandLineExecutor:
    def execute(self, command):
        return subprocess.run(command, shell=True, capture_output=True)

class Neofetch:
    def remove_colors(self, input_text):

        ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
        output_text = ansi_escape.sub('', input_text)
        return output_text

    def __init__(self):
        command = "neofetch --off --color_blocks off"
        self.executor = CommandLineExecutor()
        self.output = self.remove_colors(str(self.executor.execute(command).stdout.decode('utf-8')))



class NeofetchPlugin(PluginBase):
    executor = CommandLineExecutor()

    def __init__(self, api) -> None:
        super().__init__(api)

    async def on_command(self, event, args) -> Exception | str:
        if args[0] == "neofetch":

            if platform.system() == "Windows":
                return 'This module is not supported on Windows.'
            
            try:
                neofetch = Neofetch()
                output = neofetch.output

            except Exception as e:
                return e
            return output
