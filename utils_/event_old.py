import datetime, hashlib, hmac, requests, os
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

class EventData:

    def __init__(self, file: str, cc: str):
        if cc == "jp":
            cc = ""
        self.aws_access_key_id = "AKIAJCUP3WWCHRJDTPPQ"
        self.aws_secret_access_key = "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"
        self.region = "ap-northeast-1"
        self.service = "s3"
        self.request = "aws4_request"
        self.algorithm = "AWS4-HMAC-SHA256"
        self.domain = "nyanko-events-prd.s3.ap-northeast-1.amazonaws.com"
        self.url = f"https://{self.domain}/battlecats{cc}_production/{file}"

    def get_auth_header(self):
        output = self.algorithm + " "
        output += f"Credential={self.aws_access_key_id}/{self.get_date()}/{self.region}/{self.service}/{self.request}, "
        output += f"SignedHeaders=host;x-amz-content-sha256;x-amz-date, "
        signature = self.get_signing_key(self.get_amz_date())
        output += f"Signature={signature.hex()}"
        return output

    def get_date(self):
        return datetime.datetime.utcnow().strftime("%Y%m%d")

    def get_amz_date(self):
        return datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    def get_signing_key(self, amz: str):
        k = ("AWS4" + self.aws_secret_access_key).encode()
        k_date = self.hmacsha256(k, self.get_date())
        date_region_key = self.hmacsha256(k_date, self.region)
        date_region_service_key = self.hmacsha256(date_region_key, self.service)
        signing_key = self.hmacsha256(date_region_service_key, self.request)

        string_to_sign = self.get_string_to_sign(amz)

        final = self.hmacsha256(signing_key, string_to_sign)
        return final

    def hmacsha256(self, key: bytes, message: str) -> bytes:
        return hmac.new(key, message.encode(), hashlib.sha256).digest()

    def get_string_to_sign(self, amz: str):
        output = self.algorithm + "\n"
        output += amz + "\n"
        output += (
            self.get_date()
            + "/"
            + self.region
            + "/"
            + self.service
            + "/"
            + self.request
            + "\n"
        )
        request = self.get_canonical_request(amz)
        output += hashlib.sha256(request.encode()).hexdigest()
        return output

    def get_canonical_request(self, amz: str):
        output = "GET\n"
        output += self.get_canonical_uri() + "\n" + "\n"
        output += "host:" + self.domain + "\n"
        output += "x-amz-content-sha256:UNSIGNED-PAYLOAD\n"
        output += "x-amz-date:" + amz + "\n"
        output += "\n"
        output += "host;x-amz-content-sha256;x-amz-date\n"
        output += "UNSIGNED-PAYLOAD"
        return output

    def get_canonical_uri(self):
        return self.url.split(self.domain)[1]

    def make_request(self):
        url = self.url
        headers = {
            "accept-encoding": "gzip",
            "authorization": self.get_auth_header(),
            "connection": "keep-alive",
            "host": self.domain,
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; Pixel 2 Build/PQ3A.190801.002)",
            "x-amz-content-sha256": "UNSIGNED-PAYLOAD",
            "x-amz-date": self.get_amz_date(),
        }

        return requests.get(url, headers=headers)

    def to_file(self, target, cc: str, file: str):
        response = self.make_request()
        file = f'{cc}_{file}'
        with open(os.path.join(target,file), "wb") as f:
            f.write(response.content)


def event():
    print(yellow('Please select a Folder'))
    target = filedialog.askdirectory(initialdir = f"C:\\Users\\{os.getlogin()}\\downloads",title = "Select folder to save")
    if not target:
        print(red("No target folder selected, Return to main menu"))
        return __main__.main()
    print(f'{green("Folder selected: ")}  {target}\n')
    for cc in ["jp", "tw", "en", "kr"]:
        for file in ["sale.tsv", "gatya.tsv", "item.tsv"]:
            event_data = EventData(file=file, cc=cc)
            event_data.to_file(target, cc, file)
    print(green("Finish grabbing event file"))
