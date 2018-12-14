import base64
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import json
from Crypto.Cipher import AES
import re


def start_browser():
    """
    开启浏览器
    """
    browser = webdriver.Chrome()
    browser.get('https://music.163.com/discover/toplist')
    browser.switch_to.frame('g_iframe')

    return browser


def parse_html(browser):
    """
    获得歌曲列表
    """
    # res = browser.find_elements_by_xpath('/html//div[@id="toplist"]//div[@id="song-list-pre-cache"]//table//tr')  # 得到101个结果
    music_list = []
    soup = BeautifulSoup(browser.page_source, 'lxml')
    res_list = soup.find_all('tr', class_=['even', " "])
    for res in res_list:
        music_name = res.find('div', class_='ttc').span.a.b['title']
        print('歌名:', music_name)

        music_detail = res.find('div', class_='ttc').span.a['href']
        music_detail = re.findall(r'\d+', music_detail)[0]
        music_detail = 'https://music.163.com/weapi/v1/resource/comments/{}?csrf_token='.format(music_detail)
        print('歌曲链接:', music_detail)

        time = res.find('td', class_=' s-fc3').span.get_text()
        print('歌曲时长:', time)

        name = res.find('div', class_='text')['title']
        print('作者:', name)
        print('=====================================================')
        data = {
            "music_detail": music_detail,
            "music_name": music_name,
            "name": name,
            "time": time
        }
        music_list.append(data)

    return music_list


def save_file(data):
    """
    保存文件格式为json
    """
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")

    with open(father_path+'\\music_file\\music.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)


def AES_encrypt(text, key, iv):
    """
    加密
    """
    if type(text) == type(b'123'):
        text = text.decode('utf-8')

    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)

    iv = iv.encode('utf-8')
    key = key.encode('utf-8')
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    text = text.encode('utf-8')
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)

    return encrypt_text


def parse_token():
    """
    解析token，ASE
    """
    first_param = '{rid:"", offset:"0", total:"true", limit:"80", csrf_token:""}'
    second_param = "010001"
    third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    forth_param = "0CoJUm6Qyw8W8jud"

    iv = '0102030405060708'
    first_key = forth_param
    second_key = 16 * 'F'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    encSecKey = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"

    return h_encText, encSecKey


def get_hotcom(params, encSecKey):
    """
    获取热评
    """
    data = {
        'params': params,
        'encSecKey': encSecKey
    }
    # 同上
    pass


def run():
    browser = start_browser()
    music_list = parse_html(browser)
    save_file(music_list)
    browser.close()
    print('================+保存成功+================')
    print('获取token...')
    params, encSecKey = parse_token()
    print('params:', params)
    print('encSecKey', encSecKey)
    get_hotcom(params, encSecKey)


if __name__ == '__main__':
    run()

