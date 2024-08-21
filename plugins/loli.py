from plugin_base import PluginBase
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import SendReactionRequest
import requests
import os
from result_codes import *

api_url = "https://api.lolicon.app/setu/v2?size=original&size=regular"

def get_random_image():
    # Fetch data from the API
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        # Check if there's any data
        if data['error']:
            print(f"API error: {data['error']}")
            return

        # Extract the image URL
        image_data = data['data'][0]
        image_url = image_data['urls']['regular']

        return image_url
    except Exception as e:
        print(f"An error occurred while fetching data from the API: {e}")

class Loli(PluginBase):
    def __init__(self, api) -> None:
        super().__init__(api)
        
    async def on_command(self, event, args) -> str:
        if args[0] == "loli":
            chat = await event.get_chat()
            message = event.message
            await self.api.client.edit_message(chat, message, f'.loli **(processing)**')
            path = get_random_image()
            await self.api.client.send_file(chat, path, force_document=False)
            return COMMAND_OK_MESSAGE_REMOVE
