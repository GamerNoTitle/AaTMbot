import yaml
from parse import parse

with open('./config.yml', encoding='utf8') as f:
    config = yaml.load(f.read(), Loader=yaml.SafeLoader)

def getLink(raw_message):
    noParse = False
    url = config['api']['address']
    match raw_message:  # 匹配规则，不满足的写在后面（要解析的那些）
        case '/警报':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['alerts']
        case '/alerts':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['alerts']
        case '/新闻':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['news']
        case '/news':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['news']
        case '/活动':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['events']
        case '/events':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['events']
        case '/突击':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['sortie']
        case '/sortie':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['sortie']
        case '/地球赏金':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['ostrons']
        case '/ostrons':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['ostrons']
        case '/cetus':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['ostrons']
        case '/金星赏金':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['solaris']
        case '/solaris':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['solaris']
        case '/火卫二赏金':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['entratiSyndicate']
        case '/entrati':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['entratiSyndicate']
        case '/裂缝':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['fissures']
        case '/虚空裂缝':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['fissures']
        case '/fissures':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['fissures']
        case '/入侵':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['invasions']
        case '/invasions':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['invasions']
        case '/奸商':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['voidTrader']
        case '/虚空商人':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['voidTrader']
        case '/voidtrader':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['voidTrader']
        case '/每日特惠':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['dailyDeals']
        case '/特惠':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['dailyDeals']
        case '/darvo':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['dailyDeals']
        case '/dailydeals':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['dailyDeals']
        case '/地球时间':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['cetusCycle']
        case '/地球平原时间':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['cetusCycle']
        case '/希图斯时间':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['cetusCycle']
        case '/cetuscycle':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['cetusCycle']
        case '/舰队':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['constructionProgress']
        case '/construction':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['constructionProgress']
        case '/金星时间':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['vallisCycle']
        case '/金星平原时间':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['vallisCycle']            
        case '/valliscycle':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['vallisCycle']
        case '/午夜电波':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['nightwave']
        case '/电波':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['nightwave']
        case '/nightwave':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['nightwave']
        case '/仲裁':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['arbitration']
        case '/arbitration':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['arbitration']
        case '/火卫二时间':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['cambionCycle']
        case '/cambioncycle':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['cambionCycle']
        case '/扎里曼':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['zarimanCycle']
        case '/扎里曼派系':
            url += config['api']['warframe']
            url += config['api']['warframe-path']['zarimanCycle']
        case default:
            noParse = True
    if noParse:
        if raw_message.startswith('/市场'):
            parsed = parse('/市场 {item}', raw_message)
            url += config['api']['market']
            url += parsed['item']
            return url
        else:
            return '[ERROR] 无法识别的命令！'
    else:
        return url