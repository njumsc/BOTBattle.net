import json
import time
import os
import requests

global jsonSettings
global s

def setting_writer():
    url = ''
    userName = ''
    method = 0
    fileName = ''
    roomId = ''

    def check_userName():
        if (not userName) or (len(userName) > 10):
            return False
        for c in userName:
            if not (('0' <= c <= '9') or ('A' <= c <= 'Z') or ('a' <= c <= 'z')):
                return False
        return True
    def check_method():
        if not 0 < method <= 2:
            return False
        return True
    url = input('Game server url (ask the game admin for more info)\nurl: ')
    roomId = input('Room ID (ask the game admin for more info)\nroomid: ')
    while not check_userName():
        userName = input('Your user name (1<=length<=10, [0-9a-zA-Z] only)\nusername: ')
    # while not check_method():
    #     method = int(input('Your submit method\n\t1: inside python script\n\t2: outside script/executable\nmethod: '))
    fileName = input('Execute cmd\neg:\t./goldennum.out\nor\tpython goldennum.py\n: ')
    jsonSettings = {
        'url':url,
        'roomId':roomId,
        'userName':userName,
        # 'method':method,
        'cmd':fileName,
    }
    with open('settings.json', 'w') as File:
        File.write(json.dumps(jsonSettings, indent=4))
    print('settings writing success with')
    print(json.dumps(jsonSettings, indent=4))
    return

def chk_room():
    url = jsonSettings['url']
    roomId = jsonSettings['roomId']
    status = s.get(url + 'roomStatus/', params={"roomid":roomId})
    print(status.text)
    if (status.text != 'on'):
        print("Fail: Room unavailable")
        print("retry in 10s")
        # time.sleep(10)
        # chk_room()

def chk_user():
    url = jsonSettings['url']
    userName = jsonSettings['userName']
    status = s.get(url + 'userStatus/')
    if (status.text != userName):
        print("Redo login")
        s.get(url + 'userOut/')
        status = s.get(url + 'userReg/', params={"name":userName})
        print(status.text)


def proc_loop():
    chk_room()
    url = jsonSettings['url']
    roomId = jsonSettings['roomId']
    cmd = jsonSettings['cmd']
    jsonServer = json.loads(s.get(url + 'getStatus/', params={"roomid":roomId}).text)
    with open("data_last.json", "w") as File:
        File.write(json.dumps(jsonServer['history']))
    os.system(cmd)
    jsonRet = {}
    with open("rsl_last.json", "r") as File:
        jsonRet = json.loads(File.read())
    chk_user()
    jsonRet['roomid'] = roomId
    s.get(url + 'userAct/', params=jsonRet)
    return json.loads(s.get(url + 'getStatus/', params={"roomid":roomId}).text)['time']


def proc_main():
    while True:
        time.sleep(proc_loop())


if __name__ == "__main__":
    try:
        with open('settings.json', 'r') as File:
            jsonSettings = json.loads(File.read())
        print('settings loading success with')
        print(json.dumps(jsonSettings, indent=4))
    except:
        setting_writer()
    yn = input('Start? (Y/n)\n')
    if yn != 'y' and yn != 'Y':
        print('Now exit')
        exit()
    s = requests.Session()
    while True:
        try:
            proc_main()
        except Exception as inst:
            print(inst)
            print("retry in 10s")
            time.sleep(10)
