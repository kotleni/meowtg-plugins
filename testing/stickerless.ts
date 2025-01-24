import BasePlugin from "../meowtg/plugin/basePlugin";
import PluginsAPI from "../meowtg/plugin/pluginsApi";
import {Api} from "telegram";
import Message = Api.Message;
import {isMyMessage} from "../meowtg/utils";

export default class StickerlessPlugin implements BasePlugin {
    name: string = "id";
    description: string = "Get the id of the user.";
    api: PluginsAPI;

    async onLoad() {
        this.api.pluginsProcessor.registerMessagesListener(this.name, async (message) => { await this.onMessage(message); });
    }

    async onUnload() {
        this.api.pluginsProcessor.unregisterMessagesListener(this.name);
    }

    async onMessage(message: Message) {
        if(message.sticker && isMyMessage(message)) {
            await this.api.telegramClient.deleteMessages(message.chatId, [message.id], {});
        }
    }
}