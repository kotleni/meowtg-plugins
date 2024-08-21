import os
import zipfile
from plugin_base import PluginBase
from result_codes import COMMAND_OK_MESSAGE_REMOVE
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import InputMediaDocument

class BackupMe(PluginBase):
    backup_folder = '.'
    archive_path = '/tmp/meowtg-backup.zip'

    def __init__(self, header, api) -> None:
        super().__init__(header, api)

    async def load(self):
        pass

    async def on_command(self, event, args) -> str:
        if args[0] == "backup":
            # telethon client
            try:
                self.create_backup()
                # Send the backup file
                await self.send_backup(event)
                return 'Backup success.'
            except Exception as e:
                return f'Error: {str(e)}'

    def create_backup(self):
        # Create a ZIP file of the folder
        with zipfile.ZipFile(self.archive_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            for root, dirs, files in os.walk(self.backup_folder):
                dirs[:] = [d for d in dirs if d != 'env'] # Ignore env folder
                for file in files:
                    file_path = os.path.join(root, file)
                    backup_zip.write(file_path, os.path.relpath(file_path, self.backup_folder))

    async def send_backup(self, event):
        client = self.api.client

        # Open the backup file and send it
        with open(self.archive_path, 'rb') as backup_file:
            await client.send_file(
                event.chat_id,
                backup_file,
                reply_to=event.message.id
            )
