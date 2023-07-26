from pprint import pprint
from utils_ import decrypt, adb, event_old, event_new, adb_event
import inquirer, os, time, sys

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
def run(func):
    os.system('cls')
    func()
    time.sleep(5)
    os.system('cls')
    main()


def main():
    try:
        match(ask("Please Select a mode", ["Decrypt a apk", "Get server file", "Get Event File", "Exit"])):
            case "Decrypt a apk":
                run(decrypt.decrypt)
            case "Get server file":
                run(adb.adb)
            case "Get Event File":
                os.system('cls')
                match(ask("Please Select a mode", ["The old Way", "The new Way", "By ADB","Back"])):
                    case "The old Way":
                        run(event_old.event)
                    case "The new Way":
                        run(event_new.event)
                    case "By ADB":
                        run(adb_event.adb_event)
                    case "Back":
                        os.system('cls')
                        main()
            case "Exit":
                print(green('Thanks for using!'))
                time.sleep(2)
                exit(0)
    except KeyboardInterrupt:
        os.system('exit')



if __name__ == "__main__":
    sys.path.append(os.path.join(os.getcwd(), 'utils_'))
    main()