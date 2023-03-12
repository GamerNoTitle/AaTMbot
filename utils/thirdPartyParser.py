def marketParser(data: dict, *args):
    sell_data = []
    for seller in data['seller']:
        sell_data.append((seller['user']['ingame_name'],
                         seller['platinum'], seller['quantity']))
    msg = f'''===== Warframe.market 售价详情 =====
你查询的物品是 {data['word']['zh']}

为你找到了{len(sell_data)}个在线且价格较低的卖家
'''
    for seller in sell_data:
        msg += f'卖家 {seller[0]} 正在以 {seller[1]} 白金的价格进行售卖，他的手上有 {seller[2]} 件该物品\n'
    return msg


def rivenParser(data: dict, *args):
    pass
