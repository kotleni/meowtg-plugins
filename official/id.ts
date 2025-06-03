import BasePlugin from "../meowtg/plugin/basePlugin";
import {Api} from "telegram";
import Message = Api.Message;
import {getDisplayName} from "telegram/Utils";
import {showResult} from "../meowtg/utils";

export default class IdPlugin extends BasePlugin {
    name: string = "id";
    description: string = "Get the id of the user.";

    async onLoad() {
        await this.commandsProcessor
            .register(this.name, this.description, (args: string[], message: Message) => this.onIdCommand(args, message));
    }

    async onUnload() {
        this.commandsProcessor.unregister(this.name);
    }

    private async onIdCommand(args: string[], message: Message) {
        if(message.replyTo) { // If reply
            const replyMessage = await message.getReplyMessage();
            await showResult(message, `${getDisplayName(replyMessage.sender)} id is ${replyMessage.sender.id}`);
        } else { // Self
            await showResult(message, `Mine id is ${message.sender.id}`);
        }
    }
}
