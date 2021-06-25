import json

import requests


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        # 需要传递的参数
        parmas = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【一条爱吃屎的狗的小卖铺】您的验证码是{code}。如非本人操作，请勿略本短信'.format(code=code)
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict


if __name__ == '__main__':
    yun_pian = YunPian('申请的apikey值（fdsafsdsfsdfsd3ers45f4d5f4d5f4d54s）')
    yun_pian.send_sms('发送的验证码如（2021）', '发送的手机号码（13000000000）')
