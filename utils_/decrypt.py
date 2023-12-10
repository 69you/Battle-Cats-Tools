import os, shutil, zipfile, requests
from io import BufferedReader
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from tkinter import filedialog
from utils_.func import color, ask
import __main__

class env:
    LIST = 'b484857901742afc'
    PACK = '89a0f99078419c28'
    JP_PACK = 'd754868de89d717fa9e7b06da45ae9e3'
    JP_iv = '40b2131a9f388ad4e5002a98118f6128'
    EN_PACK = '0ad39e4aeaf55aa717feb1825edef521'
    EN_iv = 'd1d7e708091941d90cdf8aa5f30bb0c2'
    TW_PACK = '313d9858a7fb939def1d7d859629087d'
    TW_iv = '0e3743eb53bf5944d1ae7e10c2e54bdf'
    KR_PACK = 'bea585eb993216ef4dcb88b625c3df98'
    KR_iv = '9b13c2121d39f1353a125fed98696649'

def split(file_path, start_byte:int, arrange:int) -> bytes:
    '''Split Pack file into readable bytes'''
    with open(file_path, 'rb') as file:
        return file.read()[start_byte:start_byte+arrange]

def delete_padding(pack_res: bytes) -> bytes:
    '''Delete the unreadable padding at the end of file'''
    padding_map = {
        b'\x00': 1, b'\x01': 1, b'\x02': 2, b'\x03': 3,
        b'\x04': 4, b'\x05': 5, b'\x06': 6, b'\x07': 7,
        b'\x08': 8, b'\t': 9, b'\n': 10, b'\x0b': 11,
        b'\x0c': 12, b'\r': 13, b'\x0e': 14, b'\x0f': 15,
        b'\x10': 16
    }
    last = pack_res[-1:]
    padding_count = padding_map.get(last, 0)
    return pack_res[:-padding_count] if padding_count > 0 else pack_res

def decrypt_pack(
        root: str,
        cc: str,
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
                if name in files and 'ImageDataLocal'in item :continue    
                chunk = split(f'{root}\\APK\\LIST_PACK\\{item}.pack', int(line.strip().split(',')[1]), int(line.strip().split(',')[2]))
                file = os.path.join(f"{root}\\assets\\{item}", name)
                if 'ImageDataLocal' in item:
                    with open(file, 'wb') as split_file:
                        split_file.write(chunk)
                        print(f'{current}. {color.green(name)} add! {color.gray("")} ')
                else:
                    try:
                        pack_res = delete_padding(AES.new(bytes.fromhex(getattr(env, f'{cc.upper()}_PACK')),AES.MODE_CBC,bytes.fromhex(getattr(env, f'{cc.upper()}_iv'))).decrypt(chunk))
                        if name in files:
                            try:
                                with open(file, 'rb')as f:
                                    if f.read() != pack_res:
                                        with open(file, 'wb') as output:
                                            output.write(pack_res)
                                            print(f'{current}. {color.light_blue(f"{item}/{name}")} have been update! {color.gray("")}')
                            except FileNotFoundError:
                                with open(file, 'wb') as output:
                                    output.write(pack_res)
                                    print(f'{current}. {color.light_blue(f"{item}/{name}")} have been update! {color.gray("")}')
                        else:
                            with open(file, 'wb') as output:
                                output.write(pack_res)
                                print(f'{current}. {color.green(name)} add! {color.gray("")}')
                    except ValueError:
                        pass
                current += 1 
        except IndexError:pass


'''__main__'''
def decrypt():
    match(ask.ask("Have you installed the apk?", ["Yes", "No"])):
        case "Yes":
            print(color.yellow('Please select a APK'))
            apk = filedialog.askopenfilename(initialdir = f"C:\\Users\\{os.getlogin()}\\downloads",title = "Select file",filetypes = (("apk files","*.apk"),("all files","*.*")))
            if not apk:
                print(color.red("No APK selected, Return to main menu"))
                return __main__.main()
                # raise SystemExit(red("No APK selected"))
        case "No":
            URL = "https://d.apkpure.com/b/APK/jp.co.ponos.battlecats{}?versionCode={}0"
            info = input(f'please input country_code and version with a space\n Ex: {color.yellow("jp 12.6.1")}')
            cc = info.split(" ")[0]
            version = info.split[1]
            if (cc.lower() != 'jp') and (cc.lower() != 'tw') and (cc.lower() != 'en') and (cc.lower() != 'kr'):
                print(color.red('Please enter a valid country code, Return to main menu'))
                return __main__.main()
            first, second, third = version.split('.')
            versions = ''.join(f'{v:0>2}' for v in (first, second, third))
            try:
                res = requests.get(
                URL.format('' if cc =="jp" else cc, versions),
                stream=True,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.5 (KHTML, like Gecko) ''Version/9.1.2 Safari/601.7.5 '
                    }
                )
                with open('./tar.apk', 'wb') as file:
                    print(f'{color.green("Downloading...")}')
                    for chunk in res.iter_content(chunk_size=1024):
                        if chunk: file.write(chunk)
                apk = f"{os.getcwd()}/tar.apk"
            except:
                print(color.red("Some Err occurred, Return to main menu"))
                try:
                    os.remove("./tar.apk")
                except:
                    pass
                return __main__.main()
    print(f'{color.green("APK selected: ")}  {apk}\n')
    print(color.yellow('Please select a Folder to save'))
    root = filedialog.askdirectory(initialdir = f"C:\\Users\\{os.getlogin()}\\downloads",title = "Select folder to save")
    if not root:
        print(color.red("No target folder selected, Return to main menu"))
        return __main__.main()
        # raise SystemExit(red("No target folder selected"))
    print(f'{color.green("Folder selected: ")}  {root}\n')
    cc = input(color.yellow('please enter the country code: ') + color.gray('(jp/tw/en/kr): '))
    if (cc.lower() != 'jp') and (cc.lower() != 'tw') and (cc.lower() != 'en') and (cc.lower() != 'kr'):
        print(color.red('Please enter a valid country code, Return to main menu'))
        return __main__.main()
        # raise SystemExit(red('Please enter a valid country code'))
    #init
    if not os.path.exists(f'{root}\\APK'):
        os.mkdir(os.path.join(root,'APK'), mode=0o777)
    if not os.path.exists(f'{root}\\assets'):
        os.mkdir(os.path.join(root,'assets'), mode=0o777)
    #copy and check file
    shutil.copyfile(apk, f'{root}\\APK\\{apk.split("/")[-1]}.zip')
    files = [file for file in zipfile.ZipFile(f'{root}\\APK\\{apk.split("/")[-1]}.zip').namelist() if (file.endswith('.pack') or file.endswith('.list'))]#  and not any(country in file for country in ['de', 'es', 'fr', 'it'])
    #move and extract file
    if not os.path.exists(f'{root}\\APK\\LIST_PACK'):
        os.mkdir(os.path.join(root,'APK','LIST_PACK'), mode=0o777)
    for file in files:
        zipfile.ZipFile(f'{root}\\APK\\{apk.split("/")[-1]}.zip').extract(file, f'{root}\\APK\\LIST_PACK')
        os.rename(f'{root}\\APK\\LIST_PACK\\{file}', f'{root}\\APK\\LIST_PACK\\{file.split("/")[-1]}')
    shutil.rmtree(f'{root}\\APK\\LIST_PACK\\assets')
    os.remove(f'{root}\\APK\\{apk.split("/")[-1]}.zip')
    if not os.path.exists(f"{root}\\APK\\txt"):
        os.makedirs(name=f"{root}\\APK\\txt",mode=0o777)
    #decrypt
    items = [pack.split('.')[0] for pack in os.listdir(f'{root}\\APK\\LIST_PACK') if pack.endswith('.pack') and os.path.isfile(pack.replace(".pack", ".list"))]
    exist_file = []
    for roots, dirs, exist_files in os.walk(f'{root}\\assets'):
        for file in exist_files:
            exist_file.append(file)
    for item in items:
        #decode list
        with open(f'{root}\\APK\\LIST_PACK\\{item}.list','rb') as in_list:
            with open(f'{root}\\APK\\txt\\{item}.txt','wb') as w_txt:
                w_txt.write(unpad(AES.new(bytes(env.LIST,'utf-8'), AES.MODE_ECB).decrypt(BufferedReader(in_list).read()), AES.block_size))
            in_list.close()
        if not os.path.exists(f'{root}\\assets\\{item}'):
            os.makedirs(name=os.path.join(root,'assets',item), mode=0o777)
        os.remove(f'{root}\\APK\\LIST_PACK\\{item}.list')
        #decrypt pack
        lines=[]
        with open (f'{root}\\APK\\txt\\{item}.txt','r') as r_txt:
            lines = r_txt.readlines()
        count = 0
        decrypt_pack(root,cc,item,lines,count,exist_file)
    #remove useless
    shutil.rmtree(f'{root}\\APK')
    path = os.path.join(root, 'assets')
    print(f"All files done! Please check {color.yellow(path)}".replace('\\','/'))
    os.system('pause')
