from flask import Flask, request
from utils.logger import logger
from utils.message import message
from utils.responseParse import *
import asyncio
import requests
import yaml
import threading
import platform
import sys
import os
import json
from pprint import pprint, pformat

# 读取配置文件
with open('./config.yml', encoding='utf8') as f:
    config = yaml.load(f.read(), Loader=yaml.SafeLoader)
    host = config['host']['address']
    port = config['host']['port']

# 创建日志对象
log = logger(config['log']['log-level'], 'AaTM.log')

# 创建Flask服务器对象
app = Flask(__name__)

# Python版本校验
version = platform.python_version_tuple()   # 获取Python版本
if int(version[1]) < 10:
    log.error(
        f'Your Python version is lower than 3.10, currently {platform.python_version()}. Please update it to 3.10+ to use this program!')
    sys.exit(1)
else:
    from utils.linkParse import getLink

# 已经推送过的入侵列表
invasions = []
if os.path.exists('invasions.txt'):
    with open('invasions.txt', encoding='utf8') as f:
        for line in f.readlines():
            invasions.append(line.replace('\n', ''))
else:
    with open('invasions.txt', 'wt') as f:
        f.close()


@app.route('/', methods=['GET', 'POST'])
def Handler():
    data = request.get_json()
    msg = message(data)
    if msg.user_id == config['options']['bot-qq']:
        if config['options']['auto-recall']['enable']:
            pass
    else:
        link = getLink(msg.message)
        if not link.startswith('https://'): content = link
        elif not 'robot' in link:
            content = json.loads(getDetail(link))
            access_protocol = link.split('/')[-1]
            json_parser = {
                'sortie': sortieParser,
                'invasions': invasionParser
            }
            content = json_parser[access_protocol](content, invasions)
        else:
            content = getDetail(link)
        msgSender(msg, content)
    return 'Hello World'


def msgSender(msg: message, content):
    if msg.type == 'private' and (msg.user_id in config['options']['private'] or '*' in config['options']['private']):
        message = f'[CQ:reply,id={msg.message_id}]{content}'
    elif msg.type == 'group' and (msg.group_id in config['options']['groups'] or '*' in config['options']['groups']):
        message = f'[CQ:reply,id={msg.message_id}][CQ:at,qq={msg.user_id}]'
    response = requests.get(f'{config["options"]["cqhttp"]["address"]}/send_msg?user_id={msg.user_id}&message_type={msg.type}&message={message}&group_id={msg.group_id}&access_token={config["options"]["cqhttp"]["access-token"]}')
    
        
def getDetail(link):    # 通过requests调用API获得详细信息
    return requests.get(link).text


if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
