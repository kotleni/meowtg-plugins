import BasePlugin from "../meowtg/plugin/basePlugin";
import {Api} from "telegram";
import Message = Api.Message;
import {showResult} from "../meowtg/utils";

export default class EvalPlugin extends BasePlugin {
    name: string = "eval";
    description: string = "Execute JS code.";

    override async onLoad() {
        await this.commandsProcessor
            .register(this.name, this.description, (args: string[], message: Message) => this.onIdCommand(args, message));
    }

    override async onUnload() {
        this.commandsProcessor.unregister(this.name);
    }

    private async onIdCommand(args: string[], message: Message) {
        const code = message.text.replace(".eval ", "");
        const result = eval(code);
        await showResult(message, result ? result : "void");
    }
}