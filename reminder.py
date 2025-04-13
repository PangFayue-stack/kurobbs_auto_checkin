import os
import sys
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from zoneinfo import ZoneInfo

import requests
from loguru import logger
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

from ext_notification import send_notification_with_title, send_notification


class Response(BaseModel):
    code: int = Field(..., alias="code", description="返回值")
    msg: str = Field(..., alias="msg", description="提示信息")
    success: Optional[bool] = Field(None, alias="success", description="token有时才有")
    data: Optional[Any] = Field(None, alias="data", description="请求成功才有")


class KurobbsClientException(Exception):
    """Custom exception for Kurobbs client errors."""
    pass


class KurobbsClient:
    FIND_ROLE_LIST_API_URL = "https://api.kurobbs.com/gamer/widget/game3/getData"

    def __init__(self, token: str):
        self.token = token
        self.result: Dict[str, str] = {}
        self.exceptions: List[Exception] = []

    def get_headers(self) -> Dict[str, str]:
        """Get the headers required for API requests."""
        return {
            "pragma": 'no-cache',
            "cache-control": 'no-cache',
            "sec-ch-ua": '"Not)A;Brand";v="99", "Android WebView";v="127", "Chromium";v="127"',
            "source": 'h5',
            "sec-ch-ua-mobile": '?1',
            "user-agent": 'Mozilla/5.0 (Linux; Android 14; 23127PN0CC Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.2 Mobile Safari/537.36 Kuro/2.2.0 KuroGameBox/2.2.0',
            "content-type": 'application/x-www-form-urlencoded',
            "accept": 'application/json, text/plain, */*',
            "devcode": '61.178.245.214, Mozilla/5.0 (Linux; Android 14; 23127PN0CC Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.2 Mobile Safari/537.36 Kuro/2.2.0 KuroGameBox/2.2.0',
            "token": self.token,
            "sec-ch-ua-platform": 'h5',
            "origin": 'https://web-static.kurobbs.com',
            "sec-fetch-site": 'same-site',
            "sec-fetch-mode": 'cors',
            "sec-fetch-dest": 'empty',
            "accept-encoding": 'gzip, deflate, br, zstd',
            "accept-language": 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            "priority": 'u=1, i',
        }

    def make_request(self, url: str, data: Dict[str, Any]) -> Response:
        """Make a POST request to the specified URL with the given data."""
        headers = self.get_headers()
        response = requests.post(url, headers=headers, data=data)
        res = Response.model_validate_json(response.content)
        logger.debug(res.model_dump_json(indent=2, exclude={"data"}))
        return res

    def get_game_data(self, game_id: int) -> List[Dict[str, Any]]:
        """Get the list of games for the user."""
        data = {"gameId": game_id}
        res = self.make_request(self.FIND_ROLE_LIST_API_URL, data)

        return res

    def _process_sign_action(
            self,
            action_name: str,
            action_method: Callable[[], Response],
            success_message: str,
            failure_message: str,
    ):
        """
        Handle the common logic for sign-in actions.

        :param action_name: The name of the action (used to store the result).
        :param action_method: The method to call for the sign-in action.
        :param success_message: The message to log on success.
        :param failure_message: The message to log on failure.
        """
        resp = action_method()
        logger.debug(resp)
        if not resp.success:
            self.exceptions.append(KurobbsClientException(f'{failure_message}, {resp.msg}'))
        else:
            # 处理游戏数据
            data = resp.data

            # 计算剩余结晶波片数量
            cur = data['energyData']['cur']
            total = data['energyData']['total']
            remaining = total - cur

            # 当前服务器时间戳 → datetime
            refreshTime = datetime.fromtimestamp(data['energyData']["refreshTimeStamp"])

            success_message = f"当前结晶波片数量: {cur}/{total}\n"
            if data['energyData']["refreshTimeStamp"]:
                success_message += f"预计充满时间: {refreshTime.strftime('%Y-%m-%d %H:%M:%S')}"
            else:
                success_message += "结晶波片已充满"
            logger.debug(success_message)
            self.result[action_name] = success_message
            

    def start(self):
        """Start the sign-in process."""

        self._process_sign_action(
            action_name="get_game_data",
            action_method=lambda: self.get_game_data(3),
            success_message="签到奖励签到成功",
            failure_message="获取游戏数据失败",
        )

        self._log()

    @property
    def msg(self):
        return ", ".join(self.result.values()) + "!"

    def _log(self):
        """Log the results and raise exceptions if any."""
        if msg := self.msg:
            logger.info(msg)
        if self.exceptions:
            raise KurobbsClientException("; ".join(map(str, self.exceptions)))


def configure_logger(debug: bool = False):
    """Configure the logger based on the debug mode."""
    logger.remove()  # Remove default logger configuration
    log_level = "DEBUG" if debug else "INFO"
    logger.add(sys.stdout, level=log_level)


def main():
    """Main function to handle command-line arguments and start the sign-in process."""
    # 获取环境变量TOKEN
    token = os.getenv("TOKEN")
    # 获取环境变量DEBUG，默认为False
    debug = os.getenv("DEBUG", False)
    # 配置日志记录器，debug参数为debug
    configure_logger(debug=debug)

    try:
        # 创建KurobbsClient对象，token参数为token
        kurobbs = KurobbsClient(token)
        # 启动KurobbsClient对象
        kurobbs.start()
        
        # 如果kurobbs对象有msg属性，则发送通知
        if kurobbs.msg:
            send_notification_with_title("库街区助手", kurobbs.msg)
    except KurobbsClientException as e:
        # 如果发生KurobbsClientException异常，记录错误日志，不记录异常堆栈信息，发送通知，退出程序
        logger.error(str(e), exc_info=False)
        send_notification(str(e))
        # sys.exit(1)
    except Exception as e:
        # 如果发生其他异常，记录错误日志，发送通知，退出程序
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
