import BasePlugin from "../meowtg/plugin/basePlugin";
import { Api } from "telegram";
import Message = Api.Message;
import { showResult } from "../meowtg/utils";
import { exec } from "child_process";

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

    private cleanAnsi(text: string): string {
        return text.replace(/\x1B\[[0-?]*[ -/]*[@-~]/g, '');
    }

    private async onBashCommand(args: string[], message: Message) {
        const command = args[1];

        if (!command) {
            await showResult(message, "Please provide a command to execute. Usage: .bash <your_command>");
            return;
        }

        exec(command, async (error, stdout, stderr) => {
            if (error) {
                const cleanedErrorMessage = this.cleanAnsi(error.message);
                await showResult(message, `Error: ${cleanedErrorMessage}`);
                return;
            }
            if (stderr) {
                const cleanedStderr = this.cleanAnsi(stderr);
                await showResult(message, `Stderr: \n${cleanedStderr}`);
                return;
            }
            const cleanedStdout = this.cleanAnsi(stdout);
            await showResult(message, cleanedStdout ? `Stdout: \n${cleanedStdout}` : "Command executed, no output.");
        });
    }
}
