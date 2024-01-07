import os
import re
from plugin_base import PluginBase
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import SendReactionRequest
from pytube import YouTube

# U need to env/bin/pip install pytube for using this module
# by awlik 07.01.2024
class Video:

    def __init__(self, text, parse=True):
        url_pattern = re.compile(r'https?://\S+')
        urls = re.findall(url_pattern, text)
        url = urls[0] if parse else text
        self.file_name = 'temp.mp4'
        yt = YouTube(url)
        video = yt.streams.filter(res="720p").first()
        video.download(filename=self.file_name)

    def delete(self):
        os.remove(self.file_name)
        return True





class Help(PluginBase):
    """Youtube video downloader plugin. Try .yvideo<link> or .yvideo <reply on link>. U need to .cmd env/bin/pip install pytube for using this module"""
    enabled = True

    def __init__(self, api) -> None:
        super().__init__(api)

    async def load(self):
        pass

    async def on_command(self, event, args) -> str:
        if args[0] == "yvideo" or args[0] == 'youtube':
            chat = await event.get_chat()

            if event.reply_to:
                message = await self.api.client.get_messages(chat.id, ids=event.reply_to.reply_to_msg_id)
                video = Video(message.text)

            else:
                message = event.message
                video = Video(message.text.split()[1], parse=False)
            await self.api.client.send_file(chat, video.file_name)
            await self.api.client.delete_messages(chat, [event.message])
            video.delete()

