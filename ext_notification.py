import os

import requests
import json
from loguru import logger
from serverchan_sdk import sc_send


def send_notification(message):
    title = "库街区自动签到任务"
    send_bark_notification(title, message)
    send_server3_notification(title, message)
    send_feishu_notification(title, message)


def send_bark_notification(title, message):
    """Send a notification via Bark."""
    bark_device_key = os.getenv("BARK_DEVICE_KEY")
    bark_server_url = os.getenv("BARK_SERVER_URL")

    if not bark_device_key or not bark_server_url:
        logger.debug("Bark secrets are not set. Skipping notification.")
        return

    # 构造 Bark API URL
    url = f"{bark_server_url}/{bark_device_key}/{title}/{message}"
    try:
        requests.get(url)
    except Exception:
        pass


def send_server3_notification(title, message):
    server3_send_key = os.getenv("SERVER3_SEND_KEY")
    if server3_send_key:
        response = sc_send(server3_send_key, title, message, {"tags": "Github Action|库街区"})
        logger.debug(response)
    else:
        logger.debug("ServerChan3 send key not exists.")

def send_feishu_notification(title, message):
    """Send a notification via 飞书."""
    webhook_url = os.getenv("FEISHU_WEBHOOK_URL")

    title = title+"(local)"

    data = {
        "msg_type": "text",
        "title": title,
        "content": {
            "text": message
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    print(response.status_code, response.text)

