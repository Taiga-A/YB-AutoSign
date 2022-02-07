import sys
import base64
from io import BytesIO

sys.path.append("./ImageProcess")
sys.path.append("./NetWork")
from ImageProcess import imageProccess
from NetWork import YB_Req, AI_Req


isNotOk = True
times = 0

sign = YB_Req()
ai = AI_Req()

while(isNotOk and times <= 10):
    parImg = sign.getCaptcha()
    newimg = imageProccess(parImg)

    buffer = BytesIO()
    newimg.save(buffer, format='png')
    base64Img = str(base64.b64encode(buffer.getvalue()), 'utf-8')

    code = ai.getText(base64Img)

    if(code != None):
        res = sign.signSend(code)
        if(res["code"] == 2):
            isNotOk = False
            print("|--success", res["data"]["realName"], res["data"]["updateTime"])
    else:
        print("验证码识别失败")

    times += 1
    if(isNotOk):
        print("|--restar  {} / 10".format(times))

