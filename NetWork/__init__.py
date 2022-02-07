import requests
import urllib.parse
from PIL import Image
from io import BytesIO

import sys
sys.path.append("../Config")
from Config import MyCONFIG


class YB_Req:
    loginData = MyCONFIG.loginData

    YB_loginUrl = "https://m.yiban.cn/api/v4/passport/login"
    YB_NdUrl = "https://f.yiban.cn/iapp/index?act=iapp256743"
    ND_tokenUrl = "http://211.68.191.30/youni/getToken"
    ND_cookieUrl = "http://211.68.191.30/epidemic/index"
    ND_captchaUrl = "http://211.68.191.30/epidemic/captcha"
    ND_signUrl = "http://211.68.191.30/epidemic/student/sign"

    cookie = None

    def __YB_Login(self):
        res = requests.post(self.YB_loginUrl, headers={
            "AppVersion": "5.0.8",
            "Content-Type": "application/x-www-form-urlencoded",
        }, data=self.loginData)

        resToken = res.json()["data"]["access_token"]
        resCookie = res.cookies.get("https_waf_cookie")
        print(res.status_code, "YB Login:", {
              "token": resToken, "cookie": resCookie})
        return {"token": resToken, "cookie": resCookie}

    def __YB_getNdUrl(self, data) -> str:
        res = requests.get(self.YB_NdUrl, cookies={
            "loginToken": data["token"],
            "client": "android",
            "https_waf_cookie": data["cookie"]
        })
        resCookie = res.cookies.get("JSESSIONID")
        print(res.status_code, "YB Cookie:", resCookie)
        return resCookie

    def __ND_getToken(self, cookie) -> str:
        res = requests.get(self.ND_tokenUrl, cookies={
            "JSESSIONID": cookie,
        })
        resToken = res.json()["token"]
        print(res.status_code, "ND Token:", resToken)
        return resToken

    def __ND_getCookie(self, token) -> str:
        res = requests.get(self.ND_cookieUrl, params={
            "token": token
        })
        resCookie = ""
        if(res.cookies.get("JSESSIONID") != None):
            resCookie = res.cookies.get("JSESSIONID")
        else:
            resCookie = res.request.headers.get(
                "Cookie").split(';')[0].split('=')[1]
        print(res.status_code, "ND Cookie:", resCookie)
        return resCookie

    def __getCaptcha(self, cookie) -> Image.Image:
        res = requests.get(self.ND_captchaUrl, headers={
            "Accept": "image/webp,image/*,*/*;q=0.8"
        }, cookies={
            "JSESSIONID": cookie
        })

        return Image.open(BytesIO(res.content))

    def __ND_sign(self, cookie, code):
        data = self.__formatData(
            MyCONFIG.realName, MyCONFIG.studentId, MyCONFIG.homePath, MyCONFIG.school, MyCONFIG.realClass, code)
        res = requests.post(self.ND_signUrl, data=data, cookies={
            "JSESSIONID": cookie
        }, headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        })
        print(res.status_code, "ND_Sign msg:", res.json()["msg"])
        return res.json()

    def __formatData(self, name: str, id: str, home: str, school: str, className: str, code: str, ) -> str:
        Aname = urllib.parse.quote(name.encode("utf-8"))
        Aschool = urllib.parse.quote(school.encode('utf-8'))
        AclassName = urllib.parse.quote(className.encode('utf-8'))
        Ahome = urllib.parse.quote(home.encode('utf-8'))
        data = r"data=%7B%22realName%22%3A%22" + Aname + \
            r"%22%2C%22collegeName%22%3A%22" + Aschool + \
            r"%22%2C%22className%22%3A%22" + AclassName + \
            r"%22%2C%22studentId%22%3A%22" + id + \
            r"%22%2C%22answer%22%3A%22%7B%5C%22q1%5C%22%3A%5C%22%E6%98%AF%5C%22%2C%5C%22q2%5C%22%3A%5C%22%E6%98%AF%5C%22%2C%5C%22" + \
            r"q3%5C%22%3A%5C%22%E6%98%AF%5C%22%2C%5C%22q4%5C%22%3A%5C%22%E6%98%AF%5C%22%2C%5C%22q4_1%5C%22%3A%5C%22%5C%22%2C%5C%22" + \
            r"q5%5C%22%3A%5C%22%E6%98%AF%5C%22%2C%5C%22q6%5C%22%3A%5C%22%E6%98%AF%5C%22%2C%5C%22q6_1%5C%22%3A%5C%22%5C%22%2C%5C%22" + \
            r"position%5C%22%3A%5C%22" + Ahome + \
            r"%5C%22%7D%22%7D&captcha=" + code
        return data

    def getCaptcha(self) -> Image.Image:
        return self.__getCaptcha(self.cookie)

    def signSend(self, code) -> dict:
        return self.__ND_sign(self.cookie, code)

    def __init__(self):
        loginData = self.__YB_Login()
        ndUrlCookie = self.__YB_getNdUrl(loginData)
        ndToken = self.__ND_getToken(ndUrlCookie)
        self.cookie = self.__ND_getCookie(ndToken)


class AI_Req:
    ImgUrl = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
    tokenUrl = 'https://aip.baidubce.com/oauth/2.0/token'

    token = None

    def __init__(self) -> None:
        res = requests.post(self.tokenUrl, params={
            "grant_type": "client_credentials",
            "client_id": MyCONFIG.APIKey, 
            "client_secret": MyCONFIG.SecretKey  
        })
        if res:
            self.token = res.json()["access_token"]
            print(res.status_code, "Baidu AI Token:", self.token)
        else:
            print("Error !!!! at AI_Req -- init --")

    def getText(self, base64Img: str) -> str:
        if(self.token == None):
            print("Error !!!! Baidu AI not found token at getText")
            return None

        res = requests.post(self.ImgUrl, params={
            "access_token": self.token
        }, data={
            "image": base64Img
        }, headers={
            'content-type': 'application/x-www-form-urlencoded'
        })

        ret = None
        print(res.json())
        if res and res.json()["words_result_num"] > 0:
            ret = ""
            for item in res.json()["words_result"]:
                ret += item["words"].replace(" ", "")
            
        print(res.status_code, "Baidu AI Res:", ret)
        return ret


if __name__ == "__main__":
    print("这不是程序的正确入口, 请执行main.py")