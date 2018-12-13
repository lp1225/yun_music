import requests
from bs4 import BeautifulSoup
import time
import json


class YunSpider:
    """
    网易云音乐热歌榜
    """
    def __init__(self):
        self.base_url = 'https://music.163.com/discover/toplist?id=19723756'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Referer': 'https://music.163.com/',
            'Host': 'music.163.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
        }
        self.temp = []

    def send_request(self):
        response = requests.get(self.base_url, headers=self.headers, timeout=60)
        data = response.text
        print(data)
        return data

    def save_file(self, data):
        with open('yun.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
        print('==============+保存成功+=================')

    def parse_html(self, html):
        soup = BeautifulSoup(html)
        res_json_list = soup.find('textarea', id='song-list-pre-data').get_text()
        res_json_list = json.loads(res_json_list)
        res_dict = {}
        for res_json in res_json_list:

            res_dict['music_detail'] = 'https://music.163.com/weapi/v1/resource/comments/{}?csrf_token='.format(res_json.get('commentThreadId'))
            print('music_detail', res_json.get('commentThreadId'))

            res_dict['music_name'] = res_json.get('name')
            print('歌名:', res_json.get('name'))

            res_dict['name'] = res_json.get('artists')[0].get('name')
            print('歌手:', res_json.get('artists')[0].get('name'))

            t1 = time.localtime(res_json.get('publishTime') / 1000)
            t2 = time.strftime("%Y-%m-%d %H:%M:%S", t1)
            res_dict['created_time'] = t2
            print('歌曲发行时间:', t2)
            t3 = res_json.get('duration') / 1000
            min = int(t3 / 60)
            sec = str(int(t3 % 60))
            if len(sec) < 2:
                sec = '0' + str(sec)
            res_dict['time'] = str(min)+':'+sec
            print('歌曲时长:{}:{}'.format(min, sec))
            print('=============================================\n')
            self.temp.append(res_dict)
            res_dict = {}

    def run(self):
        html = self.send_request()
        self.parse_html(html)
        self.save_file(self.temp)


if __name__ == '__main__':
    YunSpider().run()
