import BasePlugin from "../meowtg/plugin/basePlugin";
import PluginsAPI from "../meowtg/plugin/pluginsApi";
import {Api} from "telegram";
import Message = Api.Message;
import {getDisplayName} from "telegram/Utils";

export default class IdPlugin implements BasePlugin {
    name: string = "id";
    description: string = "Get the id of the user.";
    api: PluginsAPI;

    async onLoad() {
        await this.api.commandsProcessor
            .register(this.name, this.description, (args: string[], message: Message) => this.onIdCommand(args, message));
    }

    async onUnload() {
        this.api.commandsProcessor.unregister(this.name);
    }

    private async onIdCommand(args: string[], message: Message) {
        if(message.replyTo) { // If reply
            const replyMessage = await message.getReplyMessage();
            await this.api.showResult(message, `${getDisplayName(replyMessage.sender)} id is ${replyMessage.sender.id}`);
        } else { // Self
            await this.api.showResult(message, `Mine id is ${message.sender.id}`);
        }
    }
}