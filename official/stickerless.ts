import BasePlugin from "../meowtg/plugin/basePlugin";
import {Api} from "telegram";
import Message = Api.Message;
import {isMyMessage} from "../meowtg/utils";

export default class StickerlessPlugin extends BasePlugin {
    name: string = "id";
    description: string = "Get the id of the user.";

    override async onLoad() {
        this.pluginsProcessor.registerMessagesListener(this.name, async (message) => { await this.onMessage(message); });
    }

    override async onUnload() {
        this.pluginsProcessor.unregisterMessagesListener(this.name);
    }

    async onMessage(message: Message) {
        if(message.sticker && isMyMessage(message)) {
            await this.telegramClient.deleteMessages(message.chatId, [message.id], {});
        }
    }
}