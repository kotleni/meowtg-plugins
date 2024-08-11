from plugin_base import PluginBase
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import SendReactionRequest
import requests
import os

api_url = "https://api.lolicon.app/setu/v2?size=original&size=regular"

def download_image(image_url, save_path):
    try:
        # Send a GET request to the image URL
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Check if the request was successful
        
        # Open a file in binary write mode and save the image content
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f"Image successfully downloaded: {save_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download():
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
        image_url = image_data['urls']['original']
        image_ext = image_data['ext']
        image_pid = image_data['pid']
        
        # Define the path where the image will be saved
        save_path = f"loli.{image_ext}"
        
        # Download the image
        download_image(image_url, save_path)
        return save_path
    except Exception as e:
        print(f"An error occurred while fetching data from the API: {e}")

class Loli(PluginBase):
    """User info by .user command"""
    enabled = True

    def __init__(self, api) -> None:
        super().__init__(api)
        
    async def on_command(self, event, args) -> str:
        if args[0] == "loli":
            path = download()
            await self.api.client.send_file(chat, path, force_document=False)
            return COMMAND_OK_MESSAGE_REMOVE