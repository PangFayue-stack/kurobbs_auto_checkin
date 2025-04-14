import requests
import json
import configparser
import sys
from loguru import logger

sys.path.append("..")
from ext_notification import send_notification_with_title


def qiandaorequest(headers,game_uid,url,hdid,region):
    data = {
        "act_id": hdid,
        "region": region,
        "uid": game_uid,
        "lang": "zh-cn"
    }
    response1 = requests.post(url, headers=headers, data=json.dumps(data))
    data1 = response1.text
    parsed_data1 = json.loads(data1)
    try:
        if parsed_data1["data"]["gt"] == "":
            return data1
        else:
            challenge = parsed_data1['data']['challenge']
            headers['x-rpc-challenge'] = challenge
            response = requests.post(url, headers=headers, data=json.dumps(data))
            return response.text
    except:
        return data1

def main():
    game_uid = sys.argv[1]
    hdid = sys.argv[2]
    region = sys.argv[3]
    dh = sys.argv[4]
    url = sys.argv[5]
    config = configparser.ConfigParser()
    config.read('canshu.cfg',encoding='utf-8')
    login_ticket = config['cs']['login_ticket']
    ltoken = config['cs']['ltoken']
    cookie_token = config['cs']['cookie_token']
    mys_id = config['yx']['mys_id']

    headers = {
        'x-rpc-signgame': dh,
        'Cookie':
            'login_ticket=' + login_ticket + ';' + \
            'account_id=' + mys_id + ';' + \
            'ltoken=' + ltoken + ';' + \
            'cookie_token=' + cookie_token + ';'
    }
    result = qiandaorequest(headers,game_uid,url,hdid,region)
    if '签到' in json.loads(result).get('message'):
        send_notification_with_title("米游社签到", result)
        logger.info('[原神]米游社签到成功')
    else:
        logger.error('[原神]米游社签到失败')

if __name__ == "__main__":
    main()
