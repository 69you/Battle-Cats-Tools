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

def split(file_path, start_byte:int, arrange:int) -> bytes:
    '''Split Pack file into readable bytes''' 
    with open(file_path, 'rb') as file:
        return file.read()[start_byte:start_byte+arrange]

def delete_padding(pack_res :bytes) -> bytes:
    '''delete the unreadable padding at the end of file'''
    last =  pack_res[-1:]
    if last == b'\x00':
        return pack_res[:-1]
    elif last == b'\x01':
        return pack_res[:-1]
    elif last == b'\x02':
        return pack_res[:-2]
    elif last == b'\x03':
        return pack_res[:-3]
    elif last == b'\x04':
        return pack_res[:-4]
    elif last == b'\x05':
        return pack_res[:-5]
    elif last == b'\x06':
        return pack_res[:-6]
    elif last == b'\x07':
        return pack_res[:-7]
    elif last == b'\x08':
        return pack_res[:-8]
    elif last == b'\t':
        return pack_res[:-9]
    elif last == b'\n':
        superbytetest = last[-2:]
        if superbytetest == b'\n\n':
            return pack_res[:-10]
        else:
            return pack_res
    elif last == b'\x0b':
        return pack_res[:-11]
    elif last == b'\x0c':
        return pack_res[:-12]
    elif last == b'\r':
        return pack_res[:-13]
    elif last == b'\x0e':
        return pack_res[:-14]
    elif last == b'\x0f':
        return pack_res[:-15]
    elif last == b'\x10':
        return pack_res[:-16]
    else:
        return pack_res

def decrypt_pack(
        root: str,
        item: str,
        lines: list[str],
        count,
        files: list[str]
    ):
    '''decrypt pack file'''
    current = 1
    for line in lines:
        try:
            if count!=0 or count!=int(lines[0].strip())+1:     
                name = line.strip().split(',')[0]
                if name in files and item == 'ImageDataLocal':continue   
                chunk = split(f'{root}\\LIST_PACK\\{item}.pack', int(line.strip().split(',')[1]), int(line.strip().split(',')[2]  ))
                file = os.path.join(f"{root}\\assets\\{item}", name)
                if item == 'ImageDataLocal':
                    with open(file, 'wb') as split_file:
                        split_file.write(chunk)
                        print(f'{current}. {green(name)} add! {gray("")} ')
                else:
                    try:
                        pack_res = delete_padding(AES.new(bytes(env.PACK,'utf-8'), AES.MODE_ECB).decrypt(chunk))
                        if name in files:
                            with open(file, 'rb')as f:
                                if f.read() != pack_res:
                                    with open(file, 'wb') as output:
                                        output.write(pack_res)
                                        print(f'{current}. {light_blue(f"{item}/{name}")} have been update! {gray("")}')
                        else:
                            with open(file, 'wb') as output:
                                output.write(pack_res)
                                print(f'{current}. {green(name)} add! {gray("")}')
                    except ValueError:
                        pass
                current += 1 
        except IndexError:pass

'''__main__'''
def adb():
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
    print(yellow('Please select a Folder'))
    target = filedialog.askdirectory(initialdir = f"C:\\Users\\{os.getlogin()}\\downloads",title = "Select folder to save")
    if not target:
        print(red("No target folder selected, Return to main menu"))
        return __main__.main()
    print(f'{green("Folder selected: ")}  {target}\n')
    if not os.path.exists(f'{target}\\LIST_PACK'):
        os.mkdir(os.path.join(target,'LIST_PACK'), mode=0o777)
    try:
        subprocess.run(
        f'cd "{Path.cwd()}" & \
        adb connect 127.0.0.1:62025 &  \
        for /f "tokens=*" %f in (\'adb shell "ls /data/data/jp.co.ponos.battlecats{cc}/files/*.pack /data/data/jp.co.ponos.battlecats{cc}/files/*.list" \') \
        do adb pull %f "{target}/LIST_PACK/"', 
        shell=True
        )
    except subprocess.CalledProcessError:
        pass
    os.system('cls')
    if not os.path.exists(f'{target}\\assets'):
        os.mkdir(os.path.join(target,'assets'), mode=0o777)
    if not os.path.exists(f"{target}\\txt"):
        os.mkdir(f"{target}\\txt",mode=0o777)
    items = [pack.split('.')[0] for pack in os.listdir(f'{target}\\LIST_PACK') if pack.endswith('.pack')]
    exist_file = []
    for roots, dirs, exist_files in os.walk(f'{target}\\assets'):
        for file in exist_files:
            exist_file.append(file)
    for item in items:
        #decode list
        with open(f'{target}\\LIST_PACK\\{item}.list','rb') as in_list:
            with open(f'{target}\\txt\\{item}.txt','wb') as w_txt:
                w_txt.write(unpad(AES.new(bytes(env.LIST,'utf-8'), AES.MODE_ECB).decrypt(BufferedReader(in_list).read()), AES.block_size))
            in_list.close()
        if not os.path.exists(f'{target}\\assets\\{item}'):
            os.makedirs(name=os.path.join(target,'assets',item), mode=0o777)
        #decrypt pack
        lines=[]
        with open (f'{target}\\txt\\{item}.txt','r') as r_txt:
            lines = r_txt.readlines()
        count = 0
        decrypt_pack(target,item,lines,count,exist_file)
    #remove useless
    shutil.rmtree(f'{target}\\LIST_PACK')
    shutil.rmtree(f'{target}\\txt')
    print(f"All files done! Please check {yellow(os.path.join(target, 'assets'))}".replace('\\','/'))
    os.system('pause')
