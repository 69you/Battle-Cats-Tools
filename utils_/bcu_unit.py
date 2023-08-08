import os, shutil
from tkinter import filedialog
from utils_.func import color, ask
import __main__

anime = {
    '00': 'walk',
    '01': 'idle',
    '02': 'attack',
    '03': 'kb',
}

def bcu_unit():
    print(color.yellow('Please select BCU Folder'))
    bcu_path = filedialog.askdirectory(initialdir = f"C:\\Users\\{os.getlogin()}\\downloads",title = "Select BCU folder")
    if not bcu_path:
        print(color.red("No BCU folder selected, Return to main menu"))
        return __main__.main()
    print(f'{color.green("BCU Folder selected: ")}  {bcu_path}\n')
    bcu_path = os.path.join(bcu_path,'workspace','_local','animations')
    print(color.yellow('Please select BC Assets Folder'))
    bc_assets = filedialog.askdirectory(initialdir = f"C:\\Users\\{os.getlogin()}\\downloads",title = "Select BC assets folder")
    if not bc_assets:
        print(color.red("No BC assets folder selected, Return to main menu"))
        return __main__.main()
    print(f'{color.green("BC Assets Folder selected: ")}  {bc_assets}\n')
    anime_path = f'{bc_assets}/assets/ImageDataLocal'
    sprite_path = f'{bc_assets}/assets/NumberLocal'
    unit_icon = f'{bc_assets}/assets/UnitLocal'
    enemy_icon = f'{bc_assets}/assets/ImageLocal'
    match(ask.ask("Please Select a mode", ["Move Unit", "Move Enemy","Back"])):
        case "Move Unit":
            id = input(f'{color.yellow("Please enter the unit id: ")}')
            if not id:
                print(color.red("No unit id entered, Return to main menu"))
                return __main__.main()
            print(f'{color.green("Unit id: ")}  {id}\n')
            form = input(f'{color.yellow("Please enter the unit form: ")} {color.gray("(f/c/s or 1/2/3) ")}')
            if not form:
                print(color.red("No unit form entered, Return to main menu"))
                return __main__.main()
            print(f'{color.green("Unit form: ")}  {form}\n')
            if form in ['f', 'c', 's']:
                form = form
            elif form in ['1', '2', '3']:
                form = 'f' if form == '1' else 'c' if form == '2' else 's'
            else:
                print(color.red("Invalid unit form, Return to main menu"))
                return __main__.main()
            if not os.path.exists(f'{sprite_path}/{id}_{form}.png'):
                print(color.red("No sprite or unit found, Return to main menu"))
                return __main__.main()
            if not os.path.exists(f'{bcu_path}/{id}{form}'):
                os.mkdir(f'{bcu_path}/{id}{form}')
            # sprite
            shutil.copyfile(f'{sprite_path}/{id}_{form}.png',f'{bcu_path}/{id}{form}/sprite.png')
            # icon
            try:
                shutil.copyfile(f'{unit_icon}/uni{id}_{form}00.png',f'{bcu_path}/{id}{form}/icon_deploy.png')
            except FileNotFoundError:
                print(color.light_blue("No icon_deploy.png found, using default icon_deploy"))
                shutil.copyfile('./res/icon_deploy.png',f'{bcu_path}/{id}{form}/icon_deploy.png')
            # imgcut
            try:
                shutil.copyfile(f'{anime_path}/{id}_{form}.imgcut',f'{bcu_path}/{id}{form}/imgcut.txt')
            except FileNotFoundError:
                print(color.light_blue("No imgcut found, using default imgcut"))
                shutil.copyfile('./res/imgcut.txt',f'{bcu_path}/{id}{form}/imgcut.txt')
            # mamodel
            try:
                shutil.copyfile(f'{anime_path}/{id}_{form}.mamodel',f'{bcu_path}/{id}{form}/mamodel.txt')
            except FileNotFoundError:
                print(color.light_blue("No mamodel found, using default mamodel"))
                shutil.copyfile('./res/mamodel.txt',f'{bcu_path}/{id}{form}/mamodel.txt')
            # maanim
            for _ in ['00','01','02','03']:
                try:
                    shutil.copyfile(f'{anime_path}/{id}_{form}{_}.maanim',f'{bcu_path}/{id}{form}/maanim_{anime[_]}.txt')
                except FileNotFoundError:
                    print(color.light_blue(f"No {_} maanim found, using default {_} maanim"))
                    shutil.copyfile(f'./res/maanim_{anime[_]}.txt',f'{bcu_path}/{id}{form}/maanim_{anime[_]}.txt')
            shutil.copyfile('./res/maanim_burrow_up.txt',f'{bcu_path}/{id}{form}/maanim_burrow_up.txt')
            shutil.copyfile('./res/maanim_burrow_down.txt',f'{bcu_path}/{id}{form}/maanim_burrow_down.txt')
            shutil.copyfile('./res/maanim_burrow_move.txt',f'{bcu_path}/{id}{form}/maanim_burrow_move.txt')
            print(color.green("Finish moving unit to BCU"))
        case "Move Enemy":
            id = input(f'{color.yellow("Please enter the enemy id: ")}')
            if not id:
                print(color.red("No enemy id entered, Return to main menu"))
                return __main__.main()
            print(f'{color.green("Enemy id: ")}  {id}\n')
            if not os.path.exists(f'{sprite_path}/{id}_e.png'):
                print(color.red("No sprite or enemy found, Return to main menu"))
                return __main__.main()
            if not os.path.exists(f'{bcu_path}/e_{id}'):
                os.mkdir(f'{bcu_path}/e_{id}')
            # sprite
            shutil.copyfile(f'{sprite_path}/{id}_e.png',f'{bcu_path}/e_{id}/sprite.png')
            # icon
            try:
                shutil.copyfile(f'{enemy_icon}/enemy_icon_{id}.png',f'{bcu_path}/e_{id}/icon_deploy.png')
            except FileNotFoundError:
                print(color.light_blue("No icon_deploy.png found, using default icon_deploy"))
                shutil.copyfile('./res/icon_deploy.png',f'{bcu_path}/e_{id}/icon_deploy.png')
            # imgcut
            try:
                shutil.copyfile(f'{anime_path}/{id}_e.imgcut',f'{bcu_path}/e_{id}/imgcut.txt')
            except FileNotFoundError:
                print(color.light_blue("No imgcut found, using default imgcut"))
                shutil.copyfile('./res/imgcut.txt',f'{bcu_path}/e_{id}/imgcut.txt')
            # mamodel
            try:
                shutil.copyfile(f'{anime_path}/{id}_e.mamodel',f'{bcu_path}/e_{id}/mamodel.txt')
            except FileNotFoundError:
                print(color.light_blue("No mamodel found, using default mamodel"))
                shutil.copyfile('./res/mamodel.txt',f'{bcu_path}/e_{id}/mamodel.txt')
            # maanim
            for _ in ['00','01','02','03']:
                try:
                    shutil.copyfile(f'{anime_path}/{id}_e{_}.maanim',f'{bcu_path}/e_{id}/maanim_{anime[_]}.txt')
                except FileNotFoundError:
                    print(color.light_blue(f"No {_} maanim found, using default {_} maanim"))
                    shutil.copyfile(f'./res/maanim_{anime[_]}.txt',f'{bcu_path}/e_{id}/maanim_{anime[_]}.txt')
            shutil.copyfile('./res/maanim_burrow_up.txt',f'{bcu_path}/e_{id}/maanim_burrow_up.txt')
            shutil.copyfile('./res/maanim_burrow_down.txt',f'{bcu_path}/e_{id}/maanim_burrow_down.txt')
            shutil.copyfile('./res/maanim_burrow_move.txt',f'{bcu_path}/e_{id}/maanim_burrow_move.txt')
            print(color.green("Finish moving enemy to BCU"))
        case "Back":
            os.system('cls')
            return __main__.main()
