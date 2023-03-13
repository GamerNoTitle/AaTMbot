import yaml
from parse import parse
from utils.responseParse import fourInOneCycle

with open('./config.yml', encoding='utf8') as f:
    config = yaml.load(f.read(), Loader=yaml.SafeLoader)


def getLink(raw_message, *args):
    noParse = False
    url = config['api']['official']['base-url']
    match raw_message:  # 匹配规则，不满足的写在后面（要解析的那些）
        case '!!警报':
            url += config['api']['official']['alerts']
        case '!!alerts':
            url += config['api']['official']['alerts']
        case '!!新闻':
            url += config['api']['official']['news']
        case '!!news':
            url += config['api']['official']['news']
        case '!!活动':
            url += config['api']['official']['events']
        case '!!events':
            url += config['api']['official']['events']
        case '!!突击':
            url += config['api']['official']['sortie']
        case '!!sortie':
            url += config['api']['official']['sortie']
        case '!!地球赏金':
            url = config['api']['third-party']['base-url'] + config['api']['third-party']['warframe']['ostrons']
        case '!!ostrons':
            url = config['api']['third-party']['base-url'] + config['api']['third-party']['warframe']['ostrons']
        case '!!cetus':
            url = config['api']['third-party']['base-url'] + config['api']['third-party']['warframe']['ostrons']
        case '!!金星赏金':
            url = config['api']['third-party']['base-url'] + config['api']['third-party']['warframe']['solaris']
        case '!!solaris':
            url = config['api']['third-party']['base-url'] + config['api']['third-party']['warframe']['solaris']
        case '!!火卫二赏金':
            url = config['api']['third-party']['base-url'] + config['api']['third-party']['warframe']['entratiSyndicate']
        case '!!entrati':
            url = config['api']['third-party']['base-url'] + config['api']['third-party']['warframe']['entratiSyndicate']
        case '!!裂缝':
            url += config['api']['official']['fissures']
        case '!!虚空裂缝':
            url += config['api']['official']['fissures']
        case '!!fissures':
            url += config['api']['official']['fissures']
        case '!!入侵':
            url += config['api']['official']['invasions']
        case '!!invasions':
            url += config['api']['official']['invasions']
        case '!!奸商':
            url += config['api']['official']['voidTrader']
        case '!!虚空商人':
            url += config['api']['official']['voidTrader']
        case '!!voidtrader':
            url += config['api']['official']['voidTrader']
        case '!!每日特惠':
            url += config['api']['official']['dailyDeals']
        case '!!特惠':
            url += config['api']['official']['dailyDeals']
        case '!!darvo':
            url += config['api']['official']['dailyDeals']
        case '!!dailydeals':
            url += config['api']['official']['dailyDeals']
        case '!!地球时间':
            url += config['api']['official']['cetusCycle']
        case '!!地球平原时间':
            url += config['api']['official']['cetusCycle']
        case '!!希图斯时间':
            url += config['api']['official']['cetusCycle']
        case '!!cetuscycle':
            url += config['api']['official']['cetusCycle']
        case '!!舰队':
            url += config['api']['official']['constructionProgress']
        case '!!construction':
            url += config['api']['official']['constructionProgress']
        case '!!金星时间':
            url += config['api']['official']['vallisCycle']
        case '!!金星平原时间':
            url += config['api']['official']['vallisCycle']
        case '!!valliscycle':
            url += config['api']['official']['vallisCycle']
        case '!!午夜电波':
            url += config['api']['official']['nightwave']
        case '!!电波':
            url += config['api']['official']['nightwave']
        case '!!nightwave':
            url += config['api']['official']['nightwave']
        case '!!仲裁':
            url += config['api']['official']['arbitration']
        case '!!arbitration':
            url += config['api']['official']['arbitration']
        case '!!火卫二时间':
            url += config['api']['official']['cambionCycle']
        case '!!cambioncycle':
            url += config['api']['official']['cambionCycle']
        case '!!扎里曼':
            url += config['api']['official']['zarimanCycle']
        case '!!扎里曼派系':
            url += config['api']['official']['zarimanCycle']
        case '!!zarimancycle':
            url += config['api']['official']['zarimanCycle']
        case '!!执行官':
            url += config['api']['official']['archonHunt']
        case '!!执刑官':
            url += config['api']['official']['archonHunt']
        case '!!archon':
            url += config['api']['official']['archonHunt']
        case '!!archonhunt':
            url += config['api']['official']['archonHunt']
        case '!!平原':
            cetusCycle = 'https://api.warframestat.us/pc/cetusCycle/'
            vallisCycle = 'https://api.warframestat.us/pc/vallisCycle'
            cambionCycle = 'https://api.warframestat.us/pc/cambionCycle'
            zarimanCycle = 'https://api.warframestat.us/pc/zarimanCycle'
            return fourInOneCycle(cetusCycle, vallisCycle, cambionCycle, zarimanCycle)
        case '!!cycle':
            cetusCycle = 'https://api.warframestat.us/pc/cetusCycle/'
            vallisCycle = 'https://api.warframestat.us/pc/vallisCycle'
            cambionCycle = 'https://api.warframestat.us/pc/cambionCycle'
            zarimanCycle = 'https://api.warframestat.us/pc/zarimanCycle'
            return fourInOneCycle(cetusCycle, vallisCycle, cambionCycle, zarimanCycle)
        case default:
            noParse = True
    if noParse:
        if raw_message.startswith('!!市场') or raw_message.startswith('!!market'):
            url = config['api']['third-party']['base-url'] + config['api']['third-party']['market']
            url += args[0][0]
            return url
        elif raw_message.startswith('!!紫卡') or raw_message.startswith('!!riven'):
            url = config['api']['third-party']['base-url'] + config['api']['third-party']['riven']
            url += args[0][0]
            return url
        elif raw_message.startswith('!!zariman') or raw_message.startswith('!!扎里曼赏金'): # DE开放了再改
            return '[ERROR] 无法查询扎里曼赏金，因为DE不给接口'
        else:
            return '[ERROR] 无法识别的命令！'
    else:
        return url
