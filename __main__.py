import inquirer, os, time, sys
from utils_.func import color, ask
from utils_ import decrypt, adb, event_old, event_new, adb_event, bcu_unit, bcuzip

def run(func):
    os.system('cls')
    func()
    time.sleep(5)
    os.system('cls')
    main()

def main():
    match(ask.ask("Please Select a mode", ["Decrypt a apk", "Get server file", "Get Event File", "Moving Unit to BCU", "Decrypt a bcu pack without password", "BCSFE", "Exit"])):
        case "Decrypt a apk":
            run(decrypt.decrypt)
        case "Get server file":
            run(adb.adb)
        case "Get Event File":
            os.system('cls')
            match(ask.ask("Please Select a mode", ["The old Way", "The new Way", "By ADB","Back"])):
                case "The old Way":
                    run(event_old.event)
                case "The new Way":
                    run(event_new.event)
                case "By ADB":
                    run(adb_event.adb_event)
                case "Back":
                    os.system('cls')
                    main()
        case "Moving Unit to BCU":
            run(bcu_unit.bcu_unit)
        case "Decrypt a bcu pack without password":
            run(bcuzip.bcuzip)
        case "BSCFE":
            print("Still in development, finish when I have time")
            time.sleep(2)
            os.system('cls')
            main()
        case "Exit":
            print(color.green('Thanks for using!'))
            time.sleep(2)
            exit(0)


if __name__ == "__main__":
    sys.path.append(os.path.join(os.getcwd(), 'utils_'))
    main()