from plugin_base import PluginBase
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import SendReactionRequest
from result_codes import *
import requests
import os
import random

# by awlik 13.07.2024

class DownloadCode:
    def __init__(self, code):
        url = f'https://http.cat/images/{code}.jpg'
        self.file_name = url.split('/')[-1]
        response = requests.get(url)

        if response.status_code == 200:
            with open(self.file_name, 'wb') as file:
                file.write(response.content)

        self.status = response.status_code == 200


class HttpCat(PluginBase):
    """
    http.cat is a website that provides HTTP status codes illustrated with pictures of cats.
    Each status code is accompanied by a humorous or expressive image of a cat, making it a fun way
    to learn about or reference HTTP status codes.

    Usage .httpcat <code>
    """

    enabled = True

    def __init__(self, api) -> None:
        super().__init__(api)

    async def load(self):
        pass

    async def on_command(self, event, args) -> str:
        base_url = 'https://http.cat/images/'
        chat = await event.get_chat()
        message = event.message

        if args[0] == "httpcat":
            try:
                http_code = args[1]
            except IndexError:
                return 'Usage: .httpcat <code>'

            file = DownloadCode(http_code)
            if file.status:
                await self.api.client.send_file(chat, file.file_name, force_document=False)
                return COMMAND_OK_MESSAGE_REMOVE

            return 'Unknown http code.'
