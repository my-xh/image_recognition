# -*- coding: utf-8 -*-

"""
@File    : recognition.py
@Time    : 2021/4/23 21:10
@Author  : my-xh
@Version : 1.0
@Software: PyCharm
@Desc    : 图像识别模块
"""

import requests
import base64

from abc import ABCMeta, abstractmethod

api_urls = {
    '银行卡': 'https://aip.baidubce.com/rest/2.0/ocr/v1/bankcard',
    '植物': 'https://aip.baidubce.com/rest/2.0/image-classify/v1/plant',
    '动物': 'https://aip.baidubce.com/rest/2.0/image-classify/v1/animal',
    '通用票据': 'https://aip.baidubce.com/rest/2.0/ocr/v1/receipt',
    '营业执照': 'https://aip.baidubce.com/rest/2.0/ocr/v1/business_license',
    '身份证': 'https://aip.baidubce.com/rest/2.0/ocr/v1/idcard',
    '车牌号': 'https://aip.baidubce.com/rest/2.0/ocr/v1/license_plate',
    '驾驶证': 'https://aip.baidubce.com/rest/2.0/ocr/v1/driving_license',
    '行驶证': 'https://aip.baidubce.com/rest/2.0/ocr/v1/vehicle_license',
    '车型': 'https://aip.baidubce.com/rest/2.0/image-classify/v1/car',
    'Logo': 'https://aip.baidubce.com/rest/2.0/image-classify/v2/logo',
}

# 前往 https://ai.baidu.com/ai-doc 获取 API Key 和 Secret Key
API_KEY = '你的API Key'
SEC_KEY = '你的Secret Key'

HOST = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={API_KEY}&client_secret={SEC_KEY}'


class Recognizer(metaclass=ABCMeta):
    """识别器基类"""
    host = HOST
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    def __init__(self, name, api_url):
        self.name = name
        self.api_url = api_url
        self.setup()

    def setup(self):
        self.session = requests.session()
        self.session.headers = self.headers

    def __get_access_token(self):
        # 获取access_token
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        # host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】'
        response = self.session.get(self.host)
        if response:
            return response.json()['access_token']
        else:
            return None

    def __get_b64image(self, img_file):
        """获取base64编码的图像数据"""
        try:
            with open(img_file, 'rb') as f:
                data = f.read()
            data = base64.b64encode(data)
        except:
            data = None
        return data

    def recognize(self, img_file):
        """识别图像"""
        access_token = self.__get_access_token()
        img = self.__get_b64image(img_file)
        if access_token is None:
            print('access_token获取失败，无法进行识别！')
            return
        if img is None:
            print(f'未找到{img_file}，无法进行识别！')
            return

        self.session.params.update({'access_token': access_token})
        data = {'image': img}
        response = self.session.post(self.api_url, data=data)
        data = response.json()
        return self.process(data)

    @abstractmethod
    def process(self, data):
        """数据处理"""


class BankCardRecognizer(Recognizer):
    """银行卡识别器"""

    def __init__(self):
        super().__init__(self.__dict__, api_urls['银行卡'])

    def process(self, data):
        print('正在处理银行卡数据')
        # print(data)

        data = data['result']
        # 获取银行卡类型
        bank_card_type = '不能识别'
        if data['bank_card_type'] == 1:
            bank_card_type = '借记卡'
        elif data['bank_card_type'] == 2:
            bank_card_type = '信用卡'

        processed_data = ['银行卡识别结果:', '-' * 20]
        processed_data.append(f'卡号: {data["bank_card_number"]}')
        processed_data.append(f'银行：{data["bank_name"]}')
        processed_data.append(f'类型: {bank_card_type}')

        return '\n'.join(processed_data)


class Plantrecognizer(Recognizer):
    """植物识别器"""

    def __init__(self):
        super().__init__(self.__dict__, api_urls['植物'])

    def process(self, data):
        print('正在处理植物数据')
        # print(data)

        data = data['result']
        processed_data = ['识别的植物如下:', '-' * 20]
        for idx, plant in enumerate(data):
            name = plant['name']
            score = float(plant['score'])
            txt = f'{idx + 1}. {name}\n相似度: {score:.2%}\n'
            processed_data.append(txt)

        return '\n'.join(processed_data)


class AnimalRecognizer(Recognizer):
    """动物识别器"""

    def __init__(self):
        super().__init__(self.__dict__, api_urls['动物'])

    def process(self, data):
        print('正在处理动物数据')
        # print(data)

        data = data['result']
        processed_data = ['识别的动物如下:', '-' * 20]
        for idx, animal in enumerate(data):
            name = animal['name']
            score = float(animal['score'])
            txt = f'{idx + 1}. {name}\n相似度: {score:.2%}\n'
            processed_data.append(txt)

        return '\n'.join(processed_data)


class ReceiptRecognizer(Recognizer):
    """通用票据识别器"""

    def __init__(self):
        super().__init__(self.__dict__, api_urls['通用票据'])

    def process(self, data):
        print('正在处理通用票据数据')
        # print(data)

        data = data['words_result']
        processed_data = ['通用票据识别结果:', '-' * 20, '\n']
        for word in data:
            processed_data.append(word['words'])

        return '  '.join(processed_data)


class BusinessLicenseRecognizer(Recognizer):
    """营业执照识别器"""

    def __init__(self):
        super().__init__(self.__dict__, api_urls['营业执照'])

    def process(self, data):
        print('正在处理营业执照数据')
        # print(data)

        data = data['words_result']
        processed_data = ['营业执照识别结果:', '-' * 20]
        for key, value in data.items():
            word = value['words']
            if word == '无':
                continue
            processed_data.append(f'{key}: {word}')

        return '\n'.join(processed_data)


class IdcardRecognizer(Recognizer):
    """身份证识别器"""

    def __init__(self):
        super().__init__(self.__dict__, api_urls['身份证'])

    def setup(self):
        super().setup()
        # front：身份证含照片的一面
        # back：身份证带国徽的一面
        # 自动检测身份证正反面，如果传参指定方向与图片相反，支持正常识别，
        # 返回参数image_status字段为"reversed_side"
        self.session.params.update({'id_card_side': 'front'})

    def process(self, data):
        print('正在处理身份证数据')
        # print(data)

        data = data['words_result']
        processed_data = ['身份证识别结果:', '-' * 20]
        for key, value in data.items():
            word = value['words'] if value['words'] else '无'
            processed_data.append(f'{key}: {word}')

        return '\n'.join(processed_data)


class LicensePlateRecognizer(Recognizer):
    """车牌号识别器"""

    def __init__(self):
        super().__init__(self.__dict__, api_urls['车牌号'])

    def process(self, data):
        print('正在处理车牌号数据')
        # print(data)

        data = data['words_result']
        processed_data = ['车牌号识别结果:', '-' * 20]
        processed_data.append(f'{data["number"]}')

        return '\n'.join(processed_data)


class DrivingLicenseRecognizer(Recognizer):
    """驾驶证识别器"""

    def __init__(self):
        super().__init__(self.__dict__, api_urls['驾驶证'])

    def process(self, data):
        print('正在处理驾驶证数据')
        # print(data)

        data = data['words_result']
        # 获取有效期限
        start_time = data.pop('有效期限')['words']
        end_time = data.pop('至')['words']

        processed_data = ['驾驶证识别结果:', '-' * 20]
        for key, value in data.items():
            processed_data.append(f'{key}: {value["words"]}')
        processed_data.append(f'有效期限:{start_time}至{end_time}')

        return '\n'.join(processed_data)


class VehicleLicenseRecognizer(Recognizer):
    """行驶证识别器"""

    def __init__(self):
        super().__init__(self.__dict__, api_urls['行驶证'])

    def process(self, data):
        print('正在处理行驶证数据')
        # print(data)

        data = data['words_result']
        processed_data = ['行驶证识别结果:', '-' * 20]
        for key, value in data.items():
            processed_data.append(f'{key}: {value["words"]}')

        return '\n'.join(processed_data)


class CarRecognizer(Recognizer):
    """车型识别器"""

    def __init__(self):
        super().__init__(self.__dict__, api_urls['车型'])

    def process(self, data):
        print('正在处理车型数据')
        # print(data)

        # 获取车身颜色
        color = f'车身颜色: {data["color_result"]}'

        data = data['result']
        processed_data = [color, '识别的汽车如下:', '-' * 20]
        for car in data:
            name = car['name']
            score = float(car['score'])
            year = car['year']
            txt = f'车型: {name}\n年份: {year}\n准确度: {score:.2%}\n'
            processed_data.append(txt)

        return '\n'.join(processed_data)


class LogoRecognizer(Recognizer):
    """Logo识别器"""

    def __init__(self):
        super().__init__(self.__dict__, api_urls['Logo'])

    def process(self, data):
        print('正在处理Logo数据')
        # print(data)

        # 去除重复商标，准确度取最大值
        brands = {}

        data = data['result']
        for brand in data:
            name = brand['name']
            score = float(brand['probability'])
            if name in brands and score <= brands[name]:
                continue
            brands[name] = score

        processed_data = ['识别的品牌如下:', '-' * 20]
        for name, score in brands.items():
            txt = f'品牌: {name}\n准确度: {score:.2%}\n'
            processed_data.append(txt)

        return '\n'.join(processed_data)


class RecognizerManager:
    """识别器管理者"""

    def __init__(self):
        self.__recognizes = {
            0: BankCardRecognizer(),
            1: Plantrecognizer(),
            2: AnimalRecognizer(),
            3: ReceiptRecognizer(),
            4: BusinessLicenseRecognizer(),
            5: IdcardRecognizer(),
            6: LicensePlateRecognizer(),
            7: DrivingLicenseRecognizer(),
            8: VehicleLicenseRecognizer(),
            9: CarRecognizer(),
            10: LogoRecognizer(),
        }
        self.common_recognize = AnimalRecognizer()

    def recognize(self, image, image_type):
        """根据图片类型选择适合的识别器进行识别"""
        recognizer = self.__recognizes.get(image_type, self.common_recognize)  # 如果没找到指定识别器则使用通用识别器
        return recognizer.recognize(image)


if __name__ == '__main__':
    mgr = RecognizerManager()
    imgs = ['银行卡图片.png', '植物图片.png', '动物图片.png', '通用票据图片.jpg', '营业执照.jpg',
            '身份证.jpg', '车牌图片.jpg', '驾驶证.jpg', '行驶证图片.jpg', '车图片.png', 'logo图片.png']
    for i in range(11):
        mgr.recognize(f'image/{imgs[i]}', i)
    # print(mgr.recognize('image/银行卡图片.png', 0))
    # print(mgr.recognize('image/植物图片.png', 1))
    # print(mgr.recognize('image/动物图片.png', 2))
