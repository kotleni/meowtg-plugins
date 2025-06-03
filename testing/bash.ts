import BasePlugin from "../meowtg/plugin/basePlugin";
import { Api } from "telegram";
import Message = Api.Message;
import { showResult } from "../meowtg/utils";
import { exec } from "child_process"; // Import exec

export default class BashPlugin extends BasePlugin {
    name: string = "bash";
    description: string = "Execute Bash commands.";

    override async onLoad() {
        await this.commandsProcessor
            .register(this.name, this.description, (args: string[], message: Message) => this.onBashCommand(args, message));
    }

    override async onUnload() {
        this.commandsProcessor.unregister(this.name);
    }

    private async onBashCommand(args: string[], message: Message) {
        const command = args[1]

        if (!command || command === `.${this.name}`) {
            await showResult(message, "Please provide a command to execute.");
            return;
        }

        exec(command, async (error, stdout, stderr) => {
            if (error) {
                await showResult(message, `Error: ${error.message}`);
                return;
            }
            if (stderr) {
                await showResult(message, `Stderr: ${stderr}`);
                return;
            }
            await showResult(message, stdout ? `Stdout: \n${stdout}` : "Command executed, no output.");
        });
    }
}
