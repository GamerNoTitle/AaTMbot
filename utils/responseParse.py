from utils.missionNode import missionNode
from utils.invasionsParse import invasionMission

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
