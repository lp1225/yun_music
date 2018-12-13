import requests
import json
import time
import get_params


class YunCom:
    """
    歌曲热评爬取
    """
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Referer': 'https://music.163.com/',
            'Host': 'music.163.com',
            'Upgrade-Insecure-Requests': '1',
        }
        self.temp = []
        self.result = {}

    def load_file(self):
        with open('yun.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        return json_data

    def get_url(self, json_data):
        for all_music in json_data:
            music_url = all_music.get('music_detail')
            music_name = all_music.get('music_name')
            auther_name = all_music.get('name')
            self.temp.append([music_url, music_name, auther_name])

    def get_hotcom(self, url):
        """
        发送请求, 其实只需要获取一次token就可以了
        """
        params, encSecKey = get_params.run()
        data = {
            'params': params,
            'encSecKey': encSecKey
        }
        response = requests.post(url[0], headers=self.headers, data=data)
        time.sleep(0.2)
        json_com = json.loads(response.text)
        hotcom_list = json_com['hotComments']
        com_list = []
        for com in hotcom_list:
            print('user:', com['user']['nickname'])
            print('content', com['content'])
            print('===========================')

            com_list.append({
                'com_user': com['user']['nickname'],
                'content': com['content']
            })
        # 构建保存格式
        self.result[url[1]] = com_list

    def parse_url(self):
        for base_url in self.temp:
            # print('url----', base_url)
            self.get_hotcom(base_url)

    def save_file(self, data):
        with open('hotcomment.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False)
        print('==============+保存成功+=================')

    def run(self):
        json_data = self.load_file()
        self.get_url(json_data)
        self.parse_url()
        self.save_file(self.result)


if __name__ == '__main__':
    YunCom().run()



