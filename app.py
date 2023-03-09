from flask import Flask, request
from utils.logger import logger
from utils.linkParse import getLink
import asyncio
import requests
import yaml
import threading
import platform
from pprint import pprint, pformat

app = Flask(__name__)

# 读取配置文件
with open('./config.yml', encoding='utf8') as f:
    config = yaml.load(f.read(), Loader=yaml.SafeLoader)
    host = config['host']['address']
    port = config['host']['port']
log = logger(config['log']['log-level'], 'ATM.log')

@app.route('/', methods=['GET', 'POST'])
def Handler():
    data = request.get_json()
    pprint(data)
    return 'Hello World'

def getPythonVersion(): # 获取Python版本
    return platform.python_version_tuple()

def getDetail(link):    # 通过requests调用API获得详细信息
    return requests.get(link).text


if __name__ == '__main__':
    version = getPythonVersion()
    if int(version[1]) < 10:
        log.error(f'Your Python version is lower than 3.10, currently {platform.python_version()}. Please update it to 3.10+ to use this program!')
    app.run(host=host, port=port, debug=True)