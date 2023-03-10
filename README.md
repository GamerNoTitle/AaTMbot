<div align='center'>
    <img src='http://cdn1.tianli0.top/gh/Vikutorika/newassets@master/img/Miscellaneous/AaTMbot/AaTMbot.jpg' width=25% height=25%>
	<h1>
        AaTMbot
    </h1>
    <p>
        Alerts & Tenno's Market Bot
    </p>
    <p>
        Dev: <a href='https://bili33.top'>GamerNoTitle</a> | Icon: <a href='https://github.com/Vanilluv'>Vanilluv</a>
    </p>
    <p>
        体验请加QQ：2436146394
    </p>
</div>


这是一个心血来潮写的Warframe查询用QQbot，他实现了以下功能

- 查询警报
- 查询新闻
- 查询游戏内活动
- 查询今日突击
- 查询地球、金星、火卫二赏金任务
- 查询入侵任务
- 查询奸商（虚空商人）情况
- 查询Darvo的每日特惠
- 查询地球/金星/火卫二时间
- 查询巨人战舰、豺狼战舰建设情况
- 查询午夜电波任务
- 查询仲裁警报
- 查询扎里曼占领情况
- 查询指定物品在[Warframe.market](https://warframe.market)上的物价
- 查询指定武器的紫卡在[Riven.market](https://riven.market)上的价格

本bot需要与[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)一起使用，将来可能会支持更多的bot架构

## 开始使用

首先你需要确保你的Python是3.10以上（打开bot的时候会有版本校验，至于为什么要3.10以上？主要是因为用了3.10以上才有的`match` `case`语法）

打开配置文件`config.yml`，它应该像下面这样

```yaml
host: 
  # address为监听的地址，如果要本地监听请输入localhost或者127.0.0.1，如果要部署在公网请输入0.0.0.0
  # port是监听的端口，根据自己需要修改即可
  address: 127.0.0.1
  port: 2233

log:  # log的等级，可选的为 DEBUG | INFO | WARN | ERROR | CRITICAL
  log-level: INFO

auto-push:
  # 这个是自动推送
  alerts:
    # 这一节是警报的自动推送（莲妈的赏赐之类的），enable是开关，delay是隔多久检测一次（单位是秒，不要设置得太低，我的api吃不消，自建api请忽略本提示）
    # channel是推送到什么地方，groups就是QQ群，private就是私聊，前提条件是bot要在群里/与私聊对方为好友
    enable: true
    delay: 60
    channel:
      groups: true
      private: false
  invasions:  # 暂时没做这个，现在没有什么卵用
    # 这一节是入侵，本来想做的来着但是好像并没有什么必要，先搁置了，配置的作用跟上面是一样的
    enable: true
    delay: 60
    channel:
      groups: true
      private: false

options:
  # 这里是一些配置，bot-qq就是用于发送消息的bot的QQ号（因为涉及到自动撤回所以请正确填写）
  bot-qq: 2436146394
  cqhttp: 
    # 这个是cqhttp的地址，在address处填写你的cqhttp的http监听地址，access-token处填写你的cqhttp的鉴权token
    address: http://127.0.0.1:5700
    access-token: AaTMbot
  auto-recall:  # 自动撤回
    # enable就是是否开启，delay就是隔多久进行撤回，单位是秒
    enable: true
    delay: 60
  groups:
    # 进行响应的群组，就是对哪些群组的消息进行响应，没有在这里填写群号的群组即使发送了指令也不会有相应，输入*表示对所有群组进行响应，建议输入*的同时输入你需要进行呢警报推送的群号，要不然警报推送推不过去的
    - -1
  private:
    # 进行响应的私聊，跟群组的逻辑差不多，同样用*来表示对所有响应，同样也影响警报的推送
    - -1
  operator: 
    # 机器人管理员的QQ号，管理部分还没做好
    - -1

########## Keep the following content unless you know what you are doing!!! ##########
##########               请不要修改下面的内容，除非你知道你在干什么！           ##########

api:  # api列表，一般来说请不要动这个
  address: https://wfapi.bili33.top
  warframe: /wf
  warframe-path:
    alerts: /robot/alerts # 警报
    news: /robot/news     # 新闻（好像没啥用，一般没人看的吧）
    events: /robot/events # 活动（热美亚啥的）
    sortie: /dev/sortie # 突击
    ostrons: /robot/Ostrons # 地球赏金
    solaris: /robot/Solaris # 金星赏金
    entratiSyndicate: /robot/EntratiSyndicate # 火卫二赏金
    fissures: /robot/fissures # 虚空裂缝
    flashSales: /robot/flashSales # 每日促销（商店里面的）
    invasions: /robot/invasions # 入侵
    voidTrader: /robot/voidTrader # 奸商
    dailyDeals: /robot/dailyDeals # Darvo的特惠
    earthCycle: /robot/earthCycle # 地球时间（USELESS，谁看这个呀，除非你要做蝶妹的任务）
    cetusCycle: /robot/cetusCycle # 西图斯时间（跟上面那个地球时间是不一样的）
    constructionProgress: /robot/constructionProgress # 巨人战舰和豺狼舰队
    vallisCycle: /robot/vallisCycle # 索拉里斯时间
    nightwave: /robot/nightwave # 午夜电波任务
    arbitration: /robot/arbitration # 仲裁
    cambionCycle: /robot/cambionCycle # 火卫二时间（FASS还是VOME）
    zarimanCycle: /robot/zarimanCycle # 扎里曼占领情况
  market: /wm/dev/
  riven: /rm/robot/
```

需要修改的地方在上面我标记了出来，请根据自己的需要修改

配置完你的bot后，你还需要在cqhttp里面配置，把双方对接上

在cqhttp的配置中，需要注意有几个地方

第一个地方是鉴权token，这个鉴权token可以随意更改，但是在bot的配置文件中记得改成一样的

```yaml
  access-token: 'AaTMbot'
```

第二个地方是监听的服务器（server那一节），address的HTTP监听地址是要填写在bot的配置文件中的（在bot的配置文件中需要带下`http://`协议头，cqhttp的配置里是没有的），post里面的`url`要跟bot的服务器地址和端口对上

```yaml
servers:
  # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
  #- http: # http 通信
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器

  - http: # HTTP 通信设置
      address: 0.0.0.0:5700 # HTTP监听地址
      timeout: 5      # 反向 HTTP 超时时间, 单位秒，<5 时将被忽略
      long-polling:   # 长轮询拓展
        enabled: false       # 是否开启
        max-queue-size: 2000 # 消息队列大小，0 表示不限制队列大小，谨慎使用
      middlewares:
        <<: *default # 引用默认中间件
      post:           # 反向HTTP POST地址列表
      - url: 'http://127.0.0.1:2233'                # 地址
        secret: ''             # 密钥
        max-retries: 3         # 最大重试，0 时禁用
        retries-interval: 1500 # 重试时间，单位毫秒，0 时立即
      #- url: http://127.0.0.1:5701/ # 地址
      #  secret: ''                  # 密钥
      #  max-retries: 10             # 最大重试，0 时禁用
      #  retries-interval: 1000      # 重试时间，单位毫秒，0 时立即

```

以上就是配置的简略过程，要更详细的过程要等晚点我在自己的网站上发

## 命令列表

| 命令             | 别名                                       | 功能                                                         |
| ---------------- | ------------------------------------------ | ------------------------------------------------------------ |
| !!帮助            | `!!help`                                    | 显示帮助文档                                                 |
| !!关于            | `!!about`                                   | 显示关于bot信息                                              |
| !!警报            | `!!alerts`                                  | 显示当前可用警报                                             |
| !!新闻            | `!!news`                                    | 显示Warframe官方新闻                                         |
| !!活动            | `!!events`                                  | 显示游戏内活动                                               |
| !!突击            | `!!sortie`                                  | 显示今日突击                                                 |
| !!地球赏金        | `!!ostrons` `!!cetus`                        | 显示地球赏金任务                                             |
| !!金星赏金        | `!!solaris`                                 | 显示金星赏金任务                                             |
| !!火卫二赏金      | `!!entrati`                                 | 显示火卫二赏金任务                                           |
| !!裂缝            | `!!虚空裂缝` `!!fissures`                    | 显示虚空裂缝（包括钢铁、比邻星）                             |
| !!入侵            | `!!invasions`                               | 显示可用入侵任务                                             |
| !!奸商            | `!!虚空商人` `!!voidtrader`                  | 显示奸商到达时间等信息                                       |
| !!特惠            | `!!每日特惠` `!!darvo` `!!dailydeals`         | 显示Darvo的特惠信息                                          |
| !!地球时间        | `!!希图斯时间` `!!地球平原时间` `cetuscycle` | 显示地球平原（希图斯）时间（早上/夜晚）                      |
| !!金星时间        | `!!金星平原时间` `!!valliscycle`             | 显示金星平原时间（寒冷/温暖）                                |
| !!火卫二时间      | `!!cambioncycle`                            | 显示火卫二环境（VOME/FASS）                                  |
| !!舰队            | `!!construction`                            | 显示巨人战舰和豺狼战舰建设情况                               |
| !!电波            | `!!午夜电波` `!!nightwave`                   | 显示午夜电波任务                                             |
| !!仲裁            | `!!arbitration`                             | 显示仲裁警报                                                 |
| !!扎里曼          | `!!扎里曼派系` `!!zarimancycle`              | 显示扎里曼占领情况                                           |
| !!市场 <物品名称> | `!!market <item>`                           | 查询物品在Warframe.market上的价格（截取最多前10条价格最低且在线） |
| !!紫卡 <武器名称> | `!!riven <weapon>`                          | 查询相应武器的紫卡在riven.market上的价格（截取前5条价格最低） |

## 赞助

可以在游戏内直接送我礼物，我的ID是`Gamer.bili`，当然也有传统的方法，请访问[Sponsors - 请给我钱！QWQ (bili33.top)](https://bili33.top/sponsors/)