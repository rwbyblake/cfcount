import requests
import time


# 调用codeforces API 获取对应信息
def get(method, payload):
    while True:
        try:
            r = requests.get('https://codeforces.com/api/' + method, params=payload)
            return r.json()
        except:
            print('retrying')
            time.sleep(100)


if __name__ == '__main__':
    print('download')
    dic = {'handle': 'rwbywhite', 'from': '1', 'count': '10'}
    print(dic)
    print(get('user.status', dic))
