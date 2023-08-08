import hashlib, hmac, requests, time, random, json, os
from tkinter import filedialog
from utils_.func import color
import __main__

class EventData:

    def __init__(self, file: str, cc: str):
        cc = "" if cc == "jp" else cc
        self.accountCode = None
        self.password = None
        self.passwordRefreshToken = None
        self.jwtToken = None
        self.tokenCreatedAt = None
        self.newEventLink = f"https://nyanko-events.ponosgames.com/battlecats{cc}_production/{file}?jwt="
        self.userCreateLink = "https://nyanko-backups.ponosgames.com/?action=createAccount&referenceId="
        self.passwordLink = "https://nyanko-auth.ponosgames.com/v1/users"
        # self.passwordRefreshLink = "https://nyanko-auth.ponosgames.com/v1/user/password"
        self.jwtLink = "https://nyanko-auth.ponosgames.com/v1/tokens"

    def generateRandomHex(self, length: int) -> str:
        return ''.join(random.choice('0123456789abcdef') for _ in range(length))

    def hmacSha256(self, key, content):
        return hmac.new(key, str(content).encode('utf-8'), hashlib.sha256).digest()

    def getNyankoSignature(self, json_text):
        random_data = self.generateRandomHex(64)
        return random_data + self.hmacSha256(bytes(self.accountCode + random_data, 'utf-8'), json_text).hex()

    def getPostResponse(self, url, json_text):
        headers = {
            "Nyanko-Signature": self.getNyankoSignature(json_text),
            "Nyanko-Signature-Version": "1",
            "Nyanko-Signature-Algorithm": "HMACSHA256",
            "Content-Type": "application/json",
            "Nyanko-Timestamp": str(int(time.time()* 1000)),
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; XQ-BC52 Build/61.2.A.0.447)",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip"
        }
        return requests.post(url=url, headers=headers, data=json_text.encode("utf-8"))

    def generateAccount(self):
        self.accountCode = None
        self.password = None
        self.passwordRefreshToken = None
        acc = requests.get(self.userCreateLink)
        if acc.json()['success'] == True:
            self.accountCode = acc.json()['accountId']
        passwordHeaderData = {
            'accountCode': self.accountCode,
            'accountCreatedAt': str(int(time.time())),
            'nonce': self.generateRandomHex(32),
        }
        passwordResponse = self.getPostResponse(self.passwordLink, json.dumps(passwordHeaderData).replace(" ", ""))
        if passwordResponse.json()['statusCode'] == 1:
            self.password = passwordResponse.json()['payload']['password']
            self.passwordRefreshToken = passwordResponse.json()['payload']['passwordRefreshToken']

    def generateJWTToken(self):
        if self.accountCode == None or self.password == None:
            return
        tokenData = {
            'accountCode': self.accountCode,
            'clientInfo': {
            'client':{
                'countryCode': 'ja',
                'version': '999999',
                },
            'device':{
                'model': 'XQ-BC52'
                },
            'os':{
                'type': 'android',
                'version': 'Android 13'
                }
            },
            'nonce': self.generateRandomHex(32),
            'password': self.password
        }
        tokenResponse = self.getPostResponse(self.jwtLink, json.dumps(tokenData).replace(" ", ""))
        if tokenResponse.json()['statusCode'] == 1:
            return tokenResponse.json()['payload']['token']

def event():
    print(color.yellow('Please select a Folder to save'))
    target = filedialog.askdirectory(initialdir = f"C:\\Users\\{os.getlogin()}\\downloads",title = "Select folder to save")
    if not target:
        print(color.red("No target folder selected, Return to main menu"))
        return __main__.main()
    print(f'{color.green("Folder selected: ")}  {target}\n')
    for cc in ["jp", "tw", "en", "kr"]:
        for file in ["sale.tsv", "gatya.tsv", "item.tsv"]:
            event_data = EventData(file=file, cc=cc)
            if event_data.accountCode == None or event_data.password == None or event_data.passwordRefreshToken == None:
                event_data.generateAccount()
            if event_data.jwtToken == None:
                event_data.jwtToken = event_data.generateJWTToken()
                if event_data.jwtToken != None:
                    event_data.tokenCreatedAt = int(time.time() * 1000)
            if not any([event_data.accountCode, event_data.password, event_data.passwordRefreshToken, event_data.jwtToken, event_data.tokenCreatedAt]) is None:
                file = f'{cc}_{file}'
                with open(os.path.join(target,file), "wb") as f:
                    f.write(requests.get(event_data.newEventLink + event_data.jwtToken).content)
    print(color.green("Finish grabbing event file"))
