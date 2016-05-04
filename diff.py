# encoding: utf-8
# author: xujipm
# 图片差异度检查
# step0. 使用函数set_img_0()设置需要对比的图片
# step1. 使用函数match()对比两个图片的差异度，返回值越大差异越大

from PIL import Image
import numpy as np
import requests
from io import BytesIO

imgSize = (320, 100)
img_0 = []
isConvertL = True
imgUrl0 = 'https://img.alicdn.com/imgextra/i2/505981619/TB2.zvGmFXXXXbkXXXXXXXXXXXX_!!505981619.jpg'


def get_img_from_url(url):
    return Image.open(BytesIO(requests.get(url).content))


def get_arr_from_img(img, is_convert=False, re_size=(0, 0)):
    #将图片数组化
    img = img.resize(re_size) if not re_size == (0, 0) else img
    img = img.convert('L') if is_convert else img
    return np.array(img), img.size


def set_img_0(img_url=imgUrl0):
    #设置要需要对比的原始图片
    global img_0, imgSize
    img_0, imgSize = get_arr_from_img(get_img_from_url(img_url), isConvertL)
    img_0 = img_0 > img_0.mean()
    return True


def match(img_url, _img_0=img_0):
    #和原始图片进行对比
    img_data, size = get_arr_from_img(get_img_from_url(img_url), isConvertL, imgSize)
    img_data = img_data > img_data.mean()
    diff = np.sum(abs(img_0-img_data))
    print('difference', diff,img_url,sep=' | ')
    return diff
