import os
from datetime import datetime

import requests

from ext_notification import send_notification
from datetime import datetime, timedelta


token = os.getenv("TOKEN")
url = 'https://api.kurobbs.com/gamer/widget/game3/getData'
headers = {
            "pragma": 'no-cache',
            "cache-control": 'no-cache',
            "sec-ch-ua": '"Not)A;Brand";v="99", "Android WebView";v="127", "Chromium";v="127"',
            "source": 'h5',
            "sec-ch-ua-mobile": '?1',
            "user-agent": 'Mozilla/5.0 (Linux; Android 14; 23127PN0CC Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.2 Mobile Safari/537.36 Kuro/2.2.0 KuroGameBox/2.2.0',
            "content-type": 'application/x-www-form-urlencoded',
            "accept": 'application/json, text/plain, */*',
            "devcode": '61.178.245.214, Mozilla/5.0 (Linux; Android 14; 23127PN0CC Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.2 Mobile Safari/537.36 Kuro/2.2.0 KuroGameBox/2.2.0',
            "token": token,
            "sec-ch-ua-platform": 'h5',
            "origin": 'https://web-static.kurobbs.com',
            "sec-fetch-site": 'same-site',
            "sec-fetch-mode": 'cors',
            "sec-fetch-dest": 'empty',
            "accept-encoding": 'gzip, deflate, br, zstd',
            "accept-language": 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            "priority": 'u=1, i',
        }

form_data = {
    'gameId': 3,
    'roleId': '102270934',
    'serverId': '76402e5b20be2c39f095a152090afddc',
    'sizeType': 1,
    'type': 2
}

# 发送 POST 请求
try:
    response = requests.post(url, headers=headers, data=form_data)

    # 检查响应状态码
    if response.status_code != 200:
        print('fetch error:', response.status_code, response.reason)
    else:
        rsp = response.json()
        if rsp.get('code') == 200:
            print('api rsp:', rsp)
        else:
            print('api error:', rsp)
except Exception as e:
    print('fetch error:', e)

data = response.json()['data']

# 计算剩余结晶波片数量
cur = data['energyData']['cur']
total = data['energyData']['total']
remaining = total - cur

# 每恢复一个需要 6 分钟，总共还需要的时间
minutes_needed = remaining * 6
time_needed = timedelta(minutes=minutes_needed)

# 当前服务器时间戳 → datetime
server_time = datetime.fromtimestamp(data['serverTime'])

# 预计充满的时间
full_time = server_time + time_needed

# 输出信息
print(f"当前结晶波片数量: {cur}/{total}")
print(f"还需恢复 {remaining} 个，预计充满时间：{full_time.strftime('%Y-%m-%d %H:%M:%S')}（共需 {minutes_needed} 分钟）")