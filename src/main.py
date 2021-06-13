import user
import download

rateBase = 1500


# 检查账户是否正确
def check_account(userList):
    for it in userList:
        js = download.get('user.info', {'handles': it})
        print("working on {}, status: {}, rate: {}".format(it, js['status'], js['result'][0]['rating']))


# user初始化并生成信息
def generateDate(accountList):
    userlist = []
    for it in accountList:
        User = user.user(it)
        userlist.append(User)
    date = open('E:\\project\\cfcount\\date.csv', 'w')
    for User in userlist:
        print("working on {}".format(User.user_name), end='')
        dateList = [str(User.get_current_rate() - rateBase), str(User.get_current_rate() - User.passedRate),
                    str(User.get_current_rate()), str(User.contestantNum), str(User.virtualNum)]
        date.write(",".join(dateList) + '\n')
        print("OK")
    date.close()


if __name__ == '__main__':
    print('main')
    codeforcesAccountFile = open('E:\\project\\cfcount\\account.csv', 'r')
    userlist = codeforcesAccountFile.readlines()[1:]
    codeforcesAccountFile.close()
    accountList = []
    for it in userlist:
        accountList.append(it.strip('\n'))
    generateDate(accountList)
