import os, shutil
from tkinter import filedialog
import __main__

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

anime = {
    '00': 'walk',
    '01': 'idle',
    '02': 'attack',
    '03': 'kb',
}

def bcu_unit():
    print(yellow('Please select BCU Folder'))
    bcu_path = filedialog.askdirectory(initialdir = f"C:\\Users\\{os.getlogin()}\\downloads",title = "Select BCU folder")
    # bcu_path = r'C:\Users\you\Desktop\BATTLE CAT\BCU'
    if not bcu_path:
        print(red("No BCU folder selected, Return to main menu"))
        return __main__.main()
    print(f'{green("BCU Folder selected: ")}  {bcu_path}\n')
    bcu_path = os.path.join(bcu_path,'workspace','_local','animations')
    print(yellow('Please select BC Assets Folder'))
    bc_assets = filedialog.askdirectory(initialdir = f"C:\\Users\\{os.getlogin()}\\downloads",title = "Select BC assets folder")
    # bc_assets = r'C:\Users\you\Desktop\BATTLE CAT\Battle-cat-data\jp'
    if not bc_assets:
        print(red("No BC assets folder selected, Return to main menu"))
        return __main__.main()
    print(f'{green("BC Assets Folder selected: ")}  {bc_assets}\n')
    anime_path = f'{bc_assets}/assets/ImageDataLocal'
    sprite_path = f'{bc_assets}/assets/NumberLocal'
    icon_path = f'{bc_assets}/assets/UnitLocal'
    id = input(f'{yellow("Please enter the unit id: ")}')
    if not id:
        print(red("No unit id entered, Return to main menu"))
        return __main__.main()
    print(f'{green("Unit id: ")}  {id}\n')
    form = input(f'{yellow("Please enter the unit form: ")} {gray("(f/c/s or 1/2/3) ")}')
    if not form:
        print(red("No unit form entered, Return to main menu"))
        return __main__.main()
    print(f'{green("Unit form: ")}  {form}\n')
    if form in ['f', 'c', 's']:
        form = form
    elif form in ['1', '2', '3']:
        form = 'f' if form == '1' else 'c' if form == '2' else 's'
    else:
        print(red("Invalid unit form, Return to main menu"))
        return __main__.main()
    if not os.path.exists(f'{sprite_path}/{id}_{form}.png'):
        print(red("No sprite or unit found, Return to main menu"))
        return __main__.main()
    if not os.path.exists(f'{bcu_path}/{id}{form}'):
        os.mkdir(f'{bcu_path}/{id}{form}')
    # sprite
    shutil.copyfile(f'{sprite_path}/{id}_{form}.png',f'{bcu_path}/{id}{form}/sprite.png')
    # icon
    try:
        shutil.copyfile(f'{icon_path}/uni{id}_{form}.png',f'{bcu_path}/{id}{form}/icon_deploy.png')
    except FileNotFoundError:
        print(light_blue("No icon_deploy.png found, using default icon_deploy"))
        shutil.copyfile('./res/icon_deploy.png',f'{bcu_path}/{id}{form}/icon_deploy.png')
    # imgcut
    try:
        shutil.copyfile(f'{anime_path}/{id}_{form}.imgcut',f'{bcu_path}/{id}{form}/imgcut.txt')
    except FileNotFoundError:
        print(light_blue("No imgcut found, using default imgcut"))
        shutil.copyfile('./res/imgcut.txt',f'{bcu_path}/{id}{form}/imgcut.txt')
    # mamodel
    try:
        shutil.copyfile(f'{anime_path}/{id}_{form}.mamodel',f'{bcu_path}/{id}{form}/mamodel.txt')
    except FileNotFoundError:
        print(light_blue("No mamodel found, using default mamodel"))
        shutil.copyfile('./res/mamodel.txt',f'{bcu_path}/{id}{form}/mamodel.txt')
    # maanim
    for _ in ['00','01','02','03']:
        try:
            shutil.copyfile(f'{anime_path}/{id}_{form}{_}.maanim',f'{bcu_path}/{id}{form}/maanim_{anime[_]}.txt')
        except FileNotFoundError:
            print(light_blue(f"No {_} maanim found, using default {_} maanim"))
            shutil.copyfile(f'./res/maanim_{anime[_]}.txt',f'{bcu_path}/{id}{form}/maanim_{anime[_]}.txt')
    shutil.copyfile('./res/maanim_burrow_up.txt',f'{bcu_path}/{id}{form}/maanim_burrow_up.txt')
    shutil.copyfile('./res/maanim_burrow_down.txt',f'{bcu_path}/{id}{form}/maanim_burrow_down.txt')
    shutil.copyfile('./res/maanim_burrow_move.txt',f'{bcu_path}/{id}{form}/maanim_burrow_move.txt')
    print(green("Finish moving unit to BCU"))
