import BasePlugin from "../meowtg/plugin/basePlugin";
import {Api} from "telegram";
import Message = Api.Message;
import {promises as fs} from 'fs';
import { getDisplayName } from "telegram/Utils";

// FIXME: hax
const TMP_FILE_PATH_IMAGE = '/tmp/meowtg-timermedia.png';
const TMP_FILE_PATH_VIDEO = '/tmp/meowtg-timermedia.mp4';

export default class SaveTimerMediaPlugin extends BasePlugin {
    name: string = "savetimermedia";
    description: string = "Redirect all incoming media with timer to saved messages.";

    override async onLoad() {
        this.messagesProcessor.register(this.name, (msg) => msg.media !== undefined && msg.media !== null, async (msg) => { await this.onMessage(msg); });
    }

    override async onUnload() {
        this.messagesProcessor.unregister(this.name);
    }

    private isContainsVideo(msg: Message): boolean {
        return (msg.media as any).className !== 'MessageMediaPhoto' 
            && (msg.media as any).video;
    }

    private async onMessage(msg: Message) {
        const ttlSeconds = (msg.media as any).ttlSeconds;
        if(ttlSeconds) { // If have media and ttlSeconds
            const isContainsVideo = this.isContainsVideo(msg);
            const buffer = await this.telegramClient.downloadMedia(msg.media!, { });
            const fileName = isContainsVideo ? TMP_FILE_PATH_VIDEO : TMP_FILE_PATH_IMAGE;

            await fs.writeFile(fileName, buffer!);
            this.telegramClient.sendFile((await this.telegramClient.getMe()).id, {
                file: fileName,
                caption: `Saved from ${getDisplayName(msg.sender!)}`
            });
        }
    }
}