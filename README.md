# 库街区 Auto Sign Job

你可以在每天指定的时间自动运行签到脚本(包含社区签到和奖励签到)，而无需手动操作。

本仓库fork自https://github.com/leeezep/kurobbs_auto_checkin.git

## 新增功能

### 体力提醒

获取结晶波片数量并提醒 文件夹reminder1.py用于调试。

```shell
python reminder1.py
```

如果能正常输出数据如下，则证明程序可用

> code=200 msg='请求成功' success=True data={'gameId': 3, 'userId': 15224390, 'serverTime': 1744512297, 'serverId': '76402e5b20bexxxxxxxxxxxxxxxxxxxxx', 'serverName': '鸣 潮', 'signInUrl': None, 'signInTxt': '已完成签到', 'hasSignIn': True, 'roleId': '10xxxxxxx', 'roleName': 'xxx', 'energyData': {'name': '结晶波片', 'img': 'https://web-static.kurobbs.com/gamerdata/widget/game3/energy.png', 'key': None, 'refreshTimeStamp': 1744597425, 'expireTimeStamp': None, 'value': None, 'status': 0, 'cur': 3, 'total': 240}, 'livenessData': {'name': '活跃度', 'img': 'https://web-static.kurobbs.com/gamerdata/widget/game3/liveness.png', 'key': None, 'refreshTimeStamp': None, 'expireTimeStamp': None, 'value': None, 'status': 0, 'cur': 100, 'total': 100}, 'battlePassData': [{'name': '电台等级', 'img': None, 'key': None, 'refreshTimeStamp': None, 'expireTimeStamp': None, 'value': None, 'status': 0, 'cur': 52, 'total': 0}, {'name': '本周经验', 'img': None, 'key': None, 'refreshTimeStamp': None, 'expireTimeStamp': None, 'value': None, 'status': 0, 'cur': 10000, 'total': 10000}]}

本项目的配置具体参考[原项目](https://github.com/leeezep/kurobbs_auto_checkin.git) 

### 原神米游社签到

同上的配置 需要在run workflow中设置环境变量account 和 password分别对应米游社的账号和密码用于登录。如果需要绝区零崩铁之类的签到，在`mys/main`内取消函数的注释即可

手动签到启动genshin_checkin.py

```shell
python genshin_checkin.py
```



## 注意事项

- 确保 `TOKEN` 的安全性，不要将其直接写在代码中。
- 如果需要修改定时任务的执行时间，可以编辑 [`.github/workflows/auto_sign.yaml`](https://github.com/PangFayue-stack/kurobbs_auto_checkin/blob/main/.github/workflows/auto_checkin.yaml) 文件中的 `cron` 表达式。
- 配置完成后 run workflow 中的`Energy Data Reminder`即体力提醒的工作流，时间设置是晚上7点触发。
- 如果需要修改体力提醒时间，可以修改[`.github/workflows/reminder.yaml`](https://github.com/PangFayue-stack/kurobbs_auto_checkin/blob/main/.github/workflows/reminder.yaml) 文件中的 `cron` 表达式，需要每小时提醒一次，可以改成`- cron: '0 * * * *'`。

## 特别感谢

* 本项目基于[kurobbs_auto_checkin](https://github.com/leeezep/kurobbs_auto_checkin) 做了优化和改动
* 体力提醒部分参考了 [TomyJan-API-Collection](https://github.com/TomyJan/Kuro-API-Collection) 的 API 实现。感谢TomyJan 的开源贡献
* 米游社部分参考了**[AutoLiver](https://github.com/tuotuooo/AutoLiver)** 开源的实现

## 贡献

如果你有任何改进建议或发现问题，欢迎提交 Issue 或 Pull Request.
