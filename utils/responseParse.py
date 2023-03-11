from utils.missionNode import missionNode
from utils.invasionsParse import invasionMission
import requests
import json

def sortieParser(data: dict, *args):
    node1, node2, node3 = data['variants']
    node1, node2, node3 = missionNode(node1), missionNode(node2), missionNode(node3)
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

def invasionParser(data: list, exists: list, *args): # 这个是推送用的，不是查询用的
    msg = '发现新的入侵任务！\n=================='
    exists_before = exists
    for invasion in data:
        invasionmission = invasionMission(invasion)
        if invasionmission.id not in exists:    # 未播报过的任务
            exists.append(invasionmission.id)
            if not invasionmission.vsInfestation:
                msg += f'''任务节点：{invasionmission.node}
{invasionmission.attacker} 打 {invasionmission.defender}
进攻方 {invasionmission.attacker} 提供了 {invasionmission.attackReward} 作为奖励
防守方 {invasionmission.defender} 提供了 {invasionmission.defendReward} 作为奖励
还需要 {invasionmission.requiredRuns} 次来自Tenno的协助才能够结束
'''
            else:
                msg += f'''任务节点：{invasionmission.node}
Infestation 大进攻！{invasionmission.attacker} 打 {invasionmission.defender}
防守方 {invasionmission.defender} 提供了 {invasionmission.defendReward} 作为奖励
还需要 {invasionmission.requiredRuns} 次来自Tenno的协助才能够结束
'''
    if not exists_before == exists:
        return msg

def marketParser(data: dict, *args):
    sell_data = []
    for seller in data['seller']:
        sell_data.append((seller['user']['ingame_name'], seller['platinum'], seller['quantity']))
    msg = f'''===== Warframe.market 售价详情 =====
你查询的物品是 {data['word']['zh']}
该物品的价格信息如下：
价格区间：{data['statistics']['min_price']} ~ {data['statistics']['max_price']} 白金
平均价格为：{data['statistics']['avg_price']}

为你找到了{len(sell_data)}个在线且价格较低的卖家
'''
    for seller in sell_data:
        msg += f'卖家 {seller[0]} 正在以 {seller[1]} 白金的价格进行售卖，他的手上有 {seller[2]} 件该物品\n'
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
