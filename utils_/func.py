import os, time, inquirer
import __main__

class color:
    def red(text) -> str:
        return('\033[31m' + text + '\033[0m')
    def green(text) -> str:
        return('\033[32m' + text + '\033[0m')
    def yellow(text) -> str:
        return('\033[33m' + text + '\033[0m')
    def light_blue(text) -> str:
        return('\033[36m' + text + '\033[0m')
    def gray(text) -> str:
        return('\033[37m' + text + '\033[0m')

class ask:
    def ask(message, choices):
        questions = [
            inquirer.List(
                "ans",
                message=message,
                choices=choices,
                default=None
                ),
            ]
        return inquirer.prompt(questions)["ans"]