import subprocess
import configparser

import os
import sys
from loguru import logger
from auto_checkin import configure_logger

def main():

    account = os.getenv('account')
    password = os.getenv('password')
    debug = os.getenv("DEBUG", False)
    configure_logger(debug=debug)

    if account is None or password is None:
        logger.error("[原神]请设置环境变量account和password")
        sys.exit(1)
    else:
        logger.debug(f"[原神]get account: {account} \n get password: {password}")

    subprocess.call(["python", "jm.py", account, password], cwd="./mys")
    subprocess.call(["python", "canshu_requests.py"], cwd="./mys")
    subprocess.call(["python", "main.py"], cwd="./mys")

if __name__ == "__main__":
    main()
    

