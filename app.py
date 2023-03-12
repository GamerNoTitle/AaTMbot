from flask import Flask, request
from parse import parse
from utils.logger import logger
from utils.message import message
from utils.responseParse import *
from utils.thirdPartyParser import *
from utils.const import help_msg, about_msg
from utils.autoPushTask import autoPushAlert
import time
import requests
import yaml
import platform
import sys
import os
import json
import _thread
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


@app.route('/', methods=['GET', 'POST'])
def Handler():
    data = request.get_json()
    log.info(f'收到了新的payload：{data}')
    msg = message(data)
    if msg.user_id == config['options']['bot-qq']:
        if config['options']['auto-recall']['enable'] and 'AaTMbot 发现了新的警报任务' not in msg.message:  # 自动撤回，推送类不撤回
            _thread.start_new_thread(
                autoRecall, (msg.message_id, config['options']['auto-recall']['delay']))
    else:
        if not msg.message.startswith('!!'):
            log.debug(f'检测到非命令消息 {msg.message}，进行忽略')
            return 'Hello World'    # 非命令直接忽略
        if msg.message in ['!!help', '!!帮助']:
            content = help_msg
        elif msg.message in ['!!about', '!!关于']:
            content = about_msg
        else:
            command, *args = msg.message.split(' ')
            # if command in ['/fissure', '/裂缝', '/虚空裂缝']:
            #     if len(args) == 0:
            #         link = getLink(command)
            #         content = fissureParser(json.loads(getDetail(link)), args)
            link = getLink(command)
            if not link.startswith('https://'):
                log.debug(f'已完成处理的消息 {msg.message}')
                content = link
            else:
                log.debug(f'由消息 {msg.message} 解析得到api链接 {link}')
                if f"{config['api']['third-party']['base-url']}{config['api']['third-party']['market']}" in link:
                    content = marketParser(json.loads(getDetail(link)))
                elif f"{config['api']['third-party']['base-url']}{config['api']['third-party']['riven']}" in link:
                    content = rivenParser(json.loads(getDetail(link)))
                else:
                    data = getDetail(link)
                    try:
                        content = json.loads(data)
                    except json.decoder.JSONDecodeError:
                        content = data
                    access_protocol = link.split('/')[-1].lower()
                    json_parser = {
                        'alerts': alertsParser,
                        'news': newsParser,
                        'events': eventsParser,
                        'sortie': sortieParser,
                        'ostrons': ostronsParser,
                        'solaris': solarisParser,
                        'entratisyndicate': entratiSyndicateParser,
                        'fissures': fissureParser,
                        'flashsales': flashSaleParser,
                        'invasions': invasionParser,
                        'voidtrader': voidTraderParser,
                        'dailydeals': dailyDealsParser,
                        'earthcycle': earthCycleParser,
                        'cetuscycle': cetusCycleParser,
                        'constructionprogress': constructionProgressParser,
                        'valliscycle': vallisCycleParser,
                        'nightwave': nightwaveParser,
                        'arbitration': arbitrationParser,
                        'cambioncycle': cambionCycleParser,
                        'zarimancycle': zarimanCycleParser,
                        'archonhunt': archonHuntParser
                    }
                    content = json_parser[access_protocol](content, args)
        msgSender(msg, content)
    return 'Hello World'


def autoRecall(msg_id, delay):  # 自动撤回
    log.info(f'识别到由bot发出的消息，自动撤回已开启，将在 {delay} 秒后撤回消息 {msg_id}')
    time.sleep(delay)
    response = requests.get(
        f'{config["options"]["cqhttp"]["address"]}/delete_msg?message_id={msg_id}&access_token={config["options"]["cqhttp"]["access-token"]}')
    log.debug(f'撤回消息：状态码为 {response.status_code}，返回内容为{response.text}')


def msgSender(msg: message, content):   # 消息发送
    log.debug(f'正在尝试进行消息发送……')
    if msg.type == 'private' and (msg.user_id in config['options']['private'] or 0 in config['options']['private']):
        message = f'[CQ:reply,id={msg.message_id}]{content}'
        response = requests.get(
            f'{config["options"]["cqhttp"]["address"]}/send_msg?&message_type={msg.type}&message={message}&user_id={msg.user_id}&access_token={config["options"]["cqhttp"]["access-token"]}')
        log.debug(f'通过调用链接 {config["options"]["cqhttp"]["address"]}/send_msg?&message_type={msg.type}&message={message}&user_id={msg.user_id}&access_token={config["options"]["cqhttp"]["access-token"]} 发送了消息')
    elif msg.type == 'group' and (msg.group_id in config['options']['groups'] or 0 in config['options']['groups']):
        message = f'[CQ:reply,id={msg.message_id}][CQ:at,qq={msg.user_id}]{content}'
        response = requests.get(
            f'{config["options"]["cqhttp"]["address"]}/send_msg?&message_type={msg.type}&message={message}&group_id={msg.group_id}&access_token={config["options"]["cqhttp"]["access-token"]}')
        log.debug(f'通过调用链接 {config["options"]["cqhttp"]["address"]}/send_msg?&message_type={msg.type}&message={message}&group_id={msg.group_id}&access_token={config["options"]["cqhttp"]["access-token"]} 发送了消息')


def getDetail(link):    # 通过requests调用API获得详细信息
    if 'api.warframestat.us' in link:
        link += '/?language=zh'
    response = requests.get(link, headers={'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'}).text
    log.debug(f'调用了 {link}，得到了如下的信息：{response}')
    return response


if __name__ == '__main__':  # 主函数
    if config['auto-push']['alerts']['enable']:
        log.info(
            f'检测到自动撤回启用，每次bot消息发送后将在 {config["options"]["auto-recall"]["delay"]} 秒后自动撤回')
        _thread.start_new_thread(autoPushAlert, (log,))
    app.run(host=host, port=port, debug=False)
