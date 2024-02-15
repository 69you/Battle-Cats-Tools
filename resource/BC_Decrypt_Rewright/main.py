import os, shutil, zipfile, requests
from io import BufferedReader
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from tkinter import filedialog

class item(item, language):
    def __init__(self, item, language):
        self.item = item
        self.language = language
        self.file_path = self.get_file_path(item)

    def get_file_path(self, item) -> str:
        '''Get file path of item'''
        return os.path.join(os.getcwd(), 'resource', 'BC_Decrypt_Rewright', 'data', self.language, item)

    def split(self, file_path, start_byte:int, arrange:int) -> bytes:
        '''Split Pack file into readable bytes'''
        with open(file_path, 'rb') as file:
            return file.read()[start_byte:start_byte+arrange]