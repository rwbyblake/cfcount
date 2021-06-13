import download
import time
import datetime
import os
import json


# 比赛信息类
class contestInfo:
    contest_file_path = 'E:\\project\\cfcount\\contest.json'
    refresh_second = 60 * 60 * 24 * 2  # 刷新间隔 目前为两天
    contest = {}

    # 初始化 判断是否需要更新
    def __init__(self):
        try:
            t = os.path.getmtime(self.contest_file_path)
            now_time = time.time()
            if now_time - t >= self.refresh_second:
                self.refresh()
        except:
            file = open(self.contest_file_path, 'w')
            file.close()
            self.refresh()

        file = open(self.contest_file_path, 'r')
        self.contest = json.load(file)
        file.close()
        print('inited, now have {} contests'.format(len(self.contest)))

    # 更新
    def refresh(self):
        print('refreshing')
        js = download.get('contest.list', {'gym': 'false'})
        file = open(self.contest_file_path, 'w')
        json.dump(self.encode(js), file)
        file.close()
        print('refreshed')

    # 重新编码
    def encode(self, js):
        js = js['result']
        encode_js = {}
        for it in js:
            encode_js[it['id']] = it
        return encode_js

    # 获取比赛时间
    def get_contest_time(self, contest_id):
        return self.contest[str(contest_id)]['startTimeSeconds']

    # 获取比赛名
    def get_contest_name(self, contest_id):
        return self.contest[str(contest_id)]['name']


if __name__ == '__main__':
    info = contestInfo()
