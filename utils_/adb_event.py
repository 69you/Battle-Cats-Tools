import os, shutil, subprocess
from io import BufferedReader
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from tkinter import filedialog
from pathlib import Path
import __main__

class env:
    LIST = 'b484857901742afc'
    PACK = '89a0f99078419c28'

files = (
    ('002a4b18244f32d7833fd81bc833b97f.dat','{}_sale.tsv'),
    ('09b1058188348630d98a08e0f731f6bd.dat','{}_gatya.tsv'),
    ('408f66def075926baea9466e70504a3b.dat','{}_daily.tsv'),
    ('523af537946b79c4f8369ed39ba78605.dat','{}_ad.json'),
)

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

package = 'jp.co.ponos.battlecats{}'

def conntect() -> str:
    '''connect to simulator (nox)'''
    for _ in [62001, 62025, 62026]:
        try:
            if f'connected to 127.0.0.1:{_}' in subprocess.check_output(f'cd "{Path.cwd()}" & adb disconnect & adb connect 127.0.0.1:{_}', shell=True).decode('utf-8', errors='replace'):
                return str(_)
                break
        except subprocess.CalledProcessError:
            pass

def check_root(port) -> bool:
    '''check if device is root'''
    try:
        if subprocess.run(f'cd "{Path.cwd()}" & adb disconnect & adb connect 127.0.0.1:{port} & adb shell su -c "echo success"', shell=True).returncode == 1:
            return True
    except Exception:
        return False

def check_apk_exist(port, cc):
    '''check if the apk is installed'''
    try:
        return package.format('' if cc == 'jp' else cc) in subprocess.check_output(f'cd "{Path.cwd()}" & adb disconnect & adb connect 127.0.0.1:{port} & adb shell ls /data/data/', shell=True).decode('utf-8')
    except subprocess.CalledProcessError:
        pass

def decrypt(
        target: str,
        file: str,
        name: str
    ):
    '''decrypt file'''
    word = '[end]'
    word2 = '}'
    with open(f'{target}\\{file}', 'rb') as f: 
        res = AES.new(bytes(env.PACK,'utf-8'), AES.MODE_ECB).decrypt(f.read())
        f.close()
        with open(f'{target}\\{name}', 'wb') as output:
            output.write(res)
            print(f'{green(name)} add! {gray("")}')
            os.remove(f'{target}\\{file}')
            if name.endswith('.tsv'):
                if word.encode() in res:
                    output.truncate(res.index(word.encode())+len(word.encode()))
            if name.endswith('.json'):
                if word2.encode() in res:
                    output.truncate(res.rfind(word2.encode())+len(word2.encode()))
            output.close()

'''__main__'''
def adb_event():
    port = conntect()
    if not port:
        print(red("No device connected, Return to main menu"))
        return __main__.main()
        # raise SystemExit(red("No device connected"))
    print(f"{green('Device detect on port')} {port}\n")
    if not check_root(port):
        print(red("Device not been root or some error occur, Return to main menu"))
        return __main__.main()
        # raise SystemExit(red("Device not been root or some error occur"))
    cc = input(yellow('please enter the country code: ') + gray('(jp/tw/en/kr): '))
    if (cc.lower() != 'jp') and (cc.lower() != 'tw') and (cc.lower() != 'en') and (cc.lower() != 'kr'):
        print(red('Please enter a valid country code, Return to main menu'))
        return __main__.main()
        # raise SystemExit(red('Please enter a valid country code'))
    if not check_apk_exist(port, cc):
        print(red('APK not installed, Return to main menu'))
        return __main__.main()
        # raise SystemExit(red(f'{cc.upper()} Version not found'))
    print(f'{green("Country Version selected: ")}  {cc}\n')
    cc = '' if cc == 'jp' else cc
    print(yellow('Please select a Folder to save'))
    target = filedialog.askdirectory(initialdir = f"C:\\Users\\{os.getlogin()}\\downloads",title = "Select folder to save")
    if not target:
        print(red("No target folder selected, Return to main menu"))
        return __main__.main()
    print(f'{green("Folder selected: ")}  {target}\n')
    for key,value in files:
        try:
            subprocess.run(
            f'cd "{Path.cwd()}" & \
            adb connect 127.0.0.1:{port} &  \
            for /f "tokens=*" %f in (\'adb shell "ls /data/data/jp.co.ponos.battlecats{cc}/files/{key}" \') \
            do adb pull %f "{target}/"', 
            shell=True
            )
        except Exception:
            print(red('Some error occur, Return to main menu'))
            return __main__.main()
    # os.system('cls')
    if cc == '': cc = 'jp'
    for _ in os.listdir(target):
        if _.endswith('.dat'):
            for key, value in files:
                if key == _:
                    decrypt(target, _, value.format(cc))
    print(f"All files done! Please check {yellow(target)}".replace('\\','/'))