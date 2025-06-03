import BasePlugin from "../meowtg/plugin/basePlugin";
import {Api} from "telegram";
import Message = Api.Message;
import Config from "../meowtg/config";
import {showResult} from "../meowtg/utils";

type StorePluginConfig = { bannedIds: string[]; warningMessage: string; }

interface SendWarningInfo {
    id: string;
    time: number;
}

const WARNING_COOLDOWN_MS = 6000;

export default class InlineBanPlugin extends BasePlugin {
    name: string = "inlineban";
    description: string = "Alternative way to ban users.";

    config: Config<StorePluginConfig>;
    lastWarnings: SendWarningInfo[] = [];

    override async onLoad() {
        const fallback: StorePluginConfig = { bannedIds: [], warningMessage: "❌ You are not allowed to text here." };
        this.config = new Config(this.name, fallback);
        await this.config.load();

        await this.commandsProcessor.register("iban", this.description, (args: string[], message: Message) => this.onBanCommand(args, message));
        await this.commandsProcessor.register("ipardon", this.description, (args: string[], message: Message) => this.onPardonCommand(args, message));
        this.pluginsProcessor.registerMessagesListener(this.name, (message: Message) => this.onMessage(message));
    }

    override async onUnload() {
        this.commandsProcessor.unregister("iban");
        this.commandsProcessor.unregister("ipardon");

        this.pluginsProcessor.unregisterMessagesListener(this.name);
    }

    private async onMessage(message: Message): Promise<void> {
        //if(!isPrivateMessageNotMine(message)) return;

        const targetId = message.chatId;
        if(this.config.model.bannedIds.find(id => id == targetId.toString())) {
            await this.telegramClient.deleteMessages(message.chatId, [message.id], {});

            const warningInfo = this.lastWarnings.find(warning => warning.id === targetId.toString());
            if(!warningInfo || Date.now() - warningInfo.time > WARNING_COOLDOWN_MS) {
                await this.telegramClient.sendMessage(message.chatId, {message: this.config.model.warningMessage});
                this.lastWarnings.push({ id: targetId.toString(), time: Date.now() });
            }
        }
    }

    private async onBanCommand(args: string[], message: Message) {
        const targetId = message.chatId;
        await showResult(message, `User with id ${targetId} has ben inline-banned.`);
        this.config.model.bannedIds.push(targetId.toString());
        await this.config.save();
    }

    private async onPardonCommand(args: string[], message: Message) {
        const targetId = message.chatId;
        await showResult(message, `User with id ${targetId} has ben inline-unbanned.`);
        this.config.model.bannedIds = this.config.model.bannedIds.filter(id => id !== targetId.toString());
        await this.config.save();
    }
}