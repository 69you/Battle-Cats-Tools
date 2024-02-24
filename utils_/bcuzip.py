import os, hashlib, json
from tkinter import filedialog
from Crypto.Cipher import AES
from utils_.func import color, ask
import __main__

def bcuzip():
    print(color.yellow("Please select a bcuzip file"))
    bcuzip = filedialog.askopenfilename(initialdir=f"C:\\Users\\{os.getlogin()}\\downloads" ,defaultextension=".bcuzip", filetypes=[("BCU Packs", "*.bcuzip")])
    if not bcuzip:
        print(color.red("No .pack.bcuzip selected, Return to main menu"))
        return __main__.main()
    print(f'{color.green(f"File selected: ")} {bcuzip}')
    root = filedialog.askdirectory(initialdir = f"C:\\Users\\{os.getlogin()}\\downloads",title = "Select folder to save")
    if not root:
        print(color.red("No target folder selected, Return to main menu"))
        return __main__.main()
    print(f'{color.green("Folder selected: ")}  {root}\n')
    pack = open(bcuzip, "rb").read()
    length = int.from_bytes(pack[0x20:0x24], "little")
    pad = 16 * (length // 16 + 1)
    aes = AES.new(pack[0x10:0x20], 2, hashlib.md5("battlecatsultimate".encode("utf-8")).digest()[0:16])
    info = json.loads(aes.decrypt(pack[0x24 : 0x24 + pad])[0:length])
    data = pack[0x24 + pad:]
    dir = info["desc"]["names"]["dat"][0]["val"]
    os.makedirs(os.path.join(root,dir), exist_ok=True)
    for _ in info["files"]:
        file = os.path.join(root, dir, *_['path'].split('/')[1:])
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "wb") as f:
            size, offset = _["size"], _["offset"]
            f.write(AES.new(pack[0x10:0x20], 2, hashlib.md5("battlecatsultimate".encode("utf-8")).digest()[0:16]).decrypt(data[offset:offset + (size + (16 - size % 16))])[:size])
    print(f'All Files Extract Finished! Please check {color.yellow(os.path.join(root,dir))}'.replace('\\','/'))