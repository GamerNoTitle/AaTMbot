import time
import yaml
import requests
import os
import json

# 读取配置文件
with open('./config.yml', encoding='utf8') as f:
    config = yaml.load(f.read(), Loader=yaml.SafeLoader)

# 已经推送过的入侵和警报列表
invasions = []
alerts = []
if os.path.exists('invasions.txt'):
    with open('invasions.txt', encoding='utf8') as f:
        for line in f.readlines():
            invasions.append(line.replace('\n', ''))
else:
    with open('invasions.txt', 'wt') as f:
        f.close()
if os.path.exists('alerts.txt'):
    with open('alerts.txt', encoding='utf8') as f:
        for line in f.readlines():
            alerts.append(line.replace('\n', ''))
else:
    with open('alerts.txt', 'wt') as f:
        f.close()


def autoPushAlert(log, *args):    # 自动推送警报任务
    log.info('警报自动推送已启用，将在有新的警报时自动推送！')
    while True:
        new_alert = False
        msg = f'AaTMbot 发现了新的警报任务！\n'
        response = requests.get(
            f"{config['api']['official']['base-url']}{config['api']['official']['alerts']}")
        data = json.loads(response.text)
        if data != []:
            log.debug('检测到当前有警报任务，正在处理……')
            for alert in data:
                if alert['id'] not in alerts:
                    new_alert = True
                    log.debug(f'检测到{alert["id"]}不在{alerts}中，即将进行推送')
                    alerts.append(alert['id'])
                    with open('alerts.txt', 'at', encoding='utf8') as f:
                        f.write(f'{alert["id"]}\n')
                    msg = msg + f'''任务地点：{alert['mission']['node']}
任务类型：{alert['mission']['type']}
任务派系：{alert['mission']['faction']} ({alert['mission']['minEnemyLevel']} - {alert['mission']['maxEnemyLevel']})
任务奖励：{alert['mission']['reward']['asString']}
剩余时间：{alert['eta']}
'''
            if new_alert:
                log.debug(f'已完成推送消息的构建：{msg}')
                log.info('有未推送的警报任务，正在进行推送……')
                if config['auto-push']['alerts']['channel']['groups']:
                    groups = config['options']['groups']
                    for group in groups:
                        requests.get(
                            f'{config["options"]["cqhttp"]["address"]}/send_msg?&message_type=group&message={msg}&group_id={group}&access_token={config["options"]["cqhttp"]["access-token"]}')
                if config['auto-push']['alerts']['channel']['private']:
                    users = config['options']['private']
                    for user in users:
                        requests.get(
                            f'{config["options"]["cqhttp"]["address"]}/send_msg?&message_type=private&message={msg}&user_id={user}&access_token={config["options"]["cqhttp"]["access-token"]}')
            else:
                log.debug('所有警报任务都已经推送过了，不再进行推送！')
        time.sleep(config['auto-push']['alerts']['delay'])
