from utils.missionNode import missionNode
from utils.invasionsParse import invasionMission
import requests
import json
import time
import datetime


def alertsParser(data: list, *args):
    class alerts:
        def __init__(self):
            pass
    msg = '目前游戏内有警报任务：\n'
    if len(data) == 0:
        return '目前没有警报任务哦~'
    for alert in data:
        cur = alerts()
        cur.node = alert['mission']['node']  # 任务点
        cur.type = alert['mission']['type']  # 任务类型
        cur.faction = alert['mission']['faction']   # 任务敌人
        cur.reward = alert['mission']['reward']['asString']  # 任务奖励
        cur.minLevel = alert['mission']['minEnemyLevel']
        cur.maxLevel = alert['mission']['maxEnemyLevel']
        cur.eta = alert['eta']
        msg += f'''任务点：{cur.node}
任务类型：{cur.type} ({cur.faction} {cur.minLevel}-{cur.maxLevel})
任务奖励：{cur.reward}
剩余时间：{cur.eta}
'''
    return msg


def newsParser(data: list, *args):
    class news:
        def __init__(self):
            pass
    if len(data) == 0:
        return '目前没有新闻哦~'
    msg = '新闻列表：\n'
    for new in data:
        cur = news()
        cur.message = new['translations']['zh']
        cur.link = new['link']
        cur.eta = new['eta']
        msg += f'''{cur.message}
{cur.link}
剩余：{cur.eta}
'''
    return msg


def eventsParser(data: list, *args):
    return '因为做的时候没有响应的活动所以这一块先搁置了~对应的API地址为：https://api.warframestat.us/pc/events/?language=zh'


def sortieParser(data: dict, *args):
    node1, node2, node3 = data['variants']
    node1, node2, node3 = missionNode(
        node1), missionNode(node2), missionNode(node3)
    msg = f'''今日突击任务内容如下
今天要打的敌方头子为{data['boss']}，派系为{data['faction']}
突击任务具体如下：

节点：{node1.node}
任务类型：{node1.type}
特殊环境：{node1.modifier}

节点：{node2.node}
任务类型：{node2.type}
特殊环境：{node2.modifier}

节点：{node3.node}
任务类型：{node3.type}
特殊环境：{node3.modifier}

剩余时间：{data['eta']}
'''
    return msg


def ostronsParser(data, *args):
    return data


def solarisParser(data, *args):
    return data


def entratiSyndicateParser(data, *args):
    return data


def fissureParser(data: dict, *args):
    if len(args) == 0:
        pass
    else:
        if args[0].lower() not in ['钢铁', '钢铁之路', 'hard', '比邻星', '九重天', '飞机', 'storm']:
            return f'[ERROR] 无效的筛选对象 {args[0]}！'
        if args[0].lower() in ['钢铁', '钢铁之路', 'hard']: # 钢铁
            pass
        else:   # 比邻星
            pass


def flashSaleParser(data: list, *args):
    class sale:
        def __init__(self):
            pass
    if len(data) == 0:
        return '目前没有特惠物品哦~'
    else:
        msg = '目前的特惠物品如下：\n'
        for item in data:
            i = sale()
            i.name = item['item']
            i.eta = item['eta']
            msg += f'''{i.name}
还剩余：{i.eta}
'''
    return msg


def invasionParser(data: list, *args):  # 这个是推送用的，不是查询用的
    if len(data) == 0:
        return '当前没有入侵任务哦~'
    msg = '当前入侵任务如下：\n'
    for mission in data:
        invasion = invasionMission(mission)
        if invasion.eta.startswith('-'):
            continue   # 筛选已经过去了的入侵
        msg += f'''====================
任务节点：{invasion.node}
由 {invasion.attacker} 打 {invasion.defender}
攻击方 {invasion.attacker} 提供了 {invasion.attackReward} 作为奖励
防守方 {invasion.defender} 提供了 {invasion.defendReward} 作为奖励
本次入侵总共需要 {invasion.requiredRuns} 次 Tenno 的协助
剩余时间：{invasion.eta}
'''
    return msg


def voidTraderParser(data: dict, *args):
    if not data['active']:
        msg = f'''奸商 {data['character']} 还没有到达哦~
他将在 {data['endString']} 后到达 {data['location']}
'''
    else:
        msg = f"奸商 {data['character']} 正在 {data['location']} 等待你的光临\n\n===== 物品列表 ====="
        for item in data['inventory']:
            msg += f'\n{item["item"]:<50} 售价 {item["ducats"]:>4} 奸商币 {item["credits"]:>8} 星币'
    return msg


def dailyDealsParser(data: list, *args):
    if len(data) == 0:
        return '当前无特惠信息，请稍后重试~'
    else:
        msg = 'AaTM 为您查询到以下来自Darvo的特惠：\n'
        for item in data:
            msg += f'''\n物品：{item['item']:<20} 
价格：{item['salePrice']}(-{item['discount']}) 白金 
存货：{item['total'] - item['sold']}/{item['total']}
剩余时间：{item['eta']}
'''
    return msg


def earthCycleParser(data: dict, *args):
    earthState = '夜晚' if not data['isDay'] else '白天'
    earthToState = '夜晚' if data['isDay'] else '白天'
    msg = f'''地球当前状态如下：
状态：{earthState}
时间：{data['timeLeft']} 到 {earthToState}
'''
    return msg


def cetusCycleParser(data: dict, *args):
    cetusState = '夜晚' if not data['isDay'] else '白天'
    cetusToState = '夜晚' if data['isDay'] else '白天'
    msg = f'''希图斯当前状态如下：
状态：{cetusState}
时间：{data['timeLeft']} 到 {cetusToState}
'''
    return msg


def constructionProgressParser(data: dict, *args):
    msg = f'''当前舰队建造情况如下：
巨人战舰(Grineer)：{data['fomorianProgress']}%
利刃豺狼舰队(Corpus)：{data['razorbackProgress']}%'''
    return msg


def vallisCycleParser(data: dict, *args):
    vallisState = '寒冷' if not data['isWarm'] else '温暖'
    vallisToState = '寒冷' if data['isWarm'] else '温暖'
    msg = f'''金星平原当前状态如下：
状态：{vallisState}
时间：{data['timeLeft']} 到 {vallisToState}
'''
    return msg


def nightwaveParser(data: dict, *args):
    msg = f'''获取到以下电波任务：\n'''
    for mission in data['activeChallenges']:
        msg += f'''[{'每日' if mission['isDaily'] else ('周常' if not mission['isElite'] else '精英')}/{mission['title']}] {mission['desc']}：{mission['reputation']} 声望\n'''
    return msg


def arbitrationParser(data: dict, *args):
    now = time.time()
    expiry = time.mktime(time.strptime(
        data['expiry'], '%Y-%m-%dT%H:%M:%S.000Z'))
    timeLeft = expiry - now
    msg = f'''获取到以下仲裁任务：
任务节点：{data['node']}
任务类型：{data['type']}
任务敌人：{data['enemy']}
'''
    return msg


def cambionCycleParser(data: dict, *args):
    cambionState = data['state'].upper()
    cambionToState = 'VOME' if data['state'] == 'fass' else 'FASS'
    msg = f'''魔胎之境当前状态如下：
状态：{cambionState}
时间：{data['timeLeft']} 到 {cambionToState}
'''
    return msg


def zarimanCycleParser(data: dict, *args):
    zarimanState = 'Grineer' if not data['isCorpus'] else 'Corpus'
    zarimanToState = 'Grineer' if data['isCorpus'] else 'Corpus'
    msg = f'''魔胎之境当前状态如下：
状态：{zarimanState}
时间：{data['timeLeft']} 到 {zarimanToState}
'''
    return msg


def archonHuntParser(data: dict, *args):
    node1, node2, node3 = data['missions']
    node1, node2, node3 = missionNode(
        node1), missionNode(node2), missionNode(node3)
    msg = f'''本周执行官任务详情如下：
本周要打的是 {data['faction']} 的 {data['boss']}

任务节点：{node1.node}
任务类型：{node1.type}

任务节点：{node2.node}
任务类型：{node2.type}

任务节点：{node3.node}
任务类型：{node3.type}

剩余时间：{data['eta']}
'''
    return msg


def fourInOneCycle(cetusCycle, VallisCycle, cambionCycle, zarimanCycle):
    cetus = json.loads(requests.get(cetusCycle).text)
    cetusToState = '夜晚' if cetus['isDay'] else '白天'
    vallis = json.loads(requests.get(VallisCycle).text)
    vallisToState = '寒冷' if vallis['isWarm'] else '温暖'
    cambion = json.loads(requests.get(cambionCycle).text)
    cambionToState = 'VOME' if cambion['state'] == 'fass' else 'FASS'
    zariman = json.loads(requests.get(zarimanCycle).text)
    zarimanToState = 'Grineer' if zariman['isCorpus'] else 'Corpus'
    msg = f'''===== 当前开放世界时间如下 =====
希图斯：{cetus['timeLeft']} 到 {cetusToState}
金星平原：{vallis['timeLeft']} 到 {vallisToState}
魔胎之境：{cambion['timeLeft']} 到 {cambionToState}
扎里曼号：{zariman['timeLeft']} 到 {zarimanToState}
'''
    return msg
