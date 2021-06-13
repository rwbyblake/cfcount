import download
import contestInfo
import time

contest_info = contestInfo.contestInfo()


# 用户类
class user:
    user_name = ''
    status_payload = {'handle': ' ', 'from': '1', 'count': '500'}
    rating_payload = {'handle': ' '}
    userInfo = {}
    passedRate = 0
    virtualNum = 0
    contestantNum = 0

    # 初始化各种信息
    def __init__(self, user_name):
        self.user_name = user_name
        self.status_payload['handle'] = user_name
        self.rating_payload['handle'] = user_name
        self.userInfo = download.get('user.info', {'handles': user_name})
        self.userInfo = self.userInfo['result'][0]
        self.passedRate = self.get_passed_rate(60 * 60 * 24 * 30)
        self.get_passed_contest_id(60 * 60 * 24 * 30)
        print("Inited {}".format(user_name))

    # 获取用户当前rate
    def get_current_rate(self):
        return self.userInfo['rating']

    # 获取距离当前时间一段时间前的rate
    def get_passed_rate(self, time_gap):
        current_time = time.time()
        rating = download.get('user.rating', self.rating_payload)['result']
        for it in rating:
            ratingTime = it['ratingUpdateTimeSeconds']
            if current_time - ratingTime < time_gap:
                return it['newRating']
        return rating[-1]['newRating']

    # 获取距离当前时间一段时间间的比赛信息
    def get_passed_contest_id(self, time_gap):
        current_time = time.time()
        submission = download.get('user.status', self.status_payload)['result']
        contestId = set()
        returnList = []
        for it in submission:
            contest_id = it['contestId']
            if str(contest_id) not in contest_info.contest:
                continue
            contest_time = contest_info.get_contest_time(contest_id)
            if current_time - contest_time > time_gap:
                continue
            contest_type = it['author']['participantType']
            if contest_type == 'VIRTUAL' or contest_type == 'CONTESTANT' or (
                    contest_type == 'PRACTICE' and it['verdict'] == 'OK'):
                if contest_id not in contestId:
                    contestId.add(contest_id)
                    returnList.append({'id': contest_id, 'type': contest_type})
                    if contest_type == 'CONTESTANT':
                        self.contestantNum = self.contestantNum + 1
                    else:
                        self.virtualNum = self.virtualNum + 1
        return returnList


if __name__ == '__main__':
    gap_time = 60 * 60 * 24 * 30
    User = user('rwbywhite')
    print(User.get_current_rate())
    print(User.get_passed_rate(gap_time))
