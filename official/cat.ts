import BasePlugin from "../meowtg/plugin/basePlugin";
import {Api} from "telegram";
import Message = Api.Message;
import InputDocumentFileLocation = Api.InputDocumentFileLocation;
import {showResult} from "../meowtg/utils";

export default class CatPlugin extends BasePlugin {
    name: string = "cat";
    description: string = "Read text files.";

    override async onLoad() {
        await this.commandsProcessor
            .register(this.name, this.description, (args: string[], message: Message) => this.onIdCommand(args, message));
    }

    override async onUnload() {
        this.commandsProcessor.unregister(this.name);
    }

    private async onIdCommand(args: string[], message: Message) {
        if(message.replyTo) { // If reply
            const replyMessage = await message.getReplyMessage();
            const doc = replyMessage.document;
            const content = await this.telegramClient.downloadFile(new InputDocumentFileLocation({
                id: doc.id,
                accessHash: doc.accessHash,
                fileReference: doc.fileReference,
                thumbSize: "y"
            }));
            const contentString = content.toString();
            if(contentString.length < 4096 - 512) {
                await showResult(message, `<code>${contentString}</code>`);
            } else {
                await showResult(message, `Error: File is too large.`);
            }
        } else { // Self
            await showResult(message, `Error: Reply to any text file.`);
        }
    }
}