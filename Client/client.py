# -*- coding: utf-8 -*-
# 换了个编码模式，之前是 cp936
import random
from client.kbdlistener import listen
from client.game import *
from client.network import *
from client.UI import *
# from client.pygamemusic import *

# 别的都不用 import

UI.垂直同步 = True
UI.宽度 = 55
UI.高度 = 60
UI.长宽改变()

游戏.消息队列 = ["现在轮到选择 长方体移动师 的玩家行动！", "选择 长方体移动师 的玩家是 pzk ！", "pzk 正在选择获得手牌或者金币"]

xjb = 玩家('xjb')
xjb.金币 = 10
xjb.角色 = '昊天金阙无上至尊自然妙有弥罗至真玉皇上帝'
xjb.英雄池 = ['泽拉斯', '狐狸', '盖伦']
xjb.手牌 = 1
xjb.积分 = 20

zer = 玩家('zer')
zer.金币 = 7
zer.角色 = '德思勤六楼的工头'
zer.英雄池 = ['卡莎', '劫', '猫']
zer.手牌 = 7
zer.积分 = 14

zxx = 玩家('zxx')
zxx.金币 = 0
zxx.角色 = '我是俊博之王'
zxx.英雄池 = ['艾希', '刀妹', '锐雯']
zxx.手牌 = 7
zxx.积分 = 36

pzk = 玩家('pzk')
pzk.金币 = 2
pzk.角色 = '长方体移动师'
pzk.英雄池 = ['阿卡丽', '艾克', '亚索']
pzk.手牌 = 0
pzk.积分 = 26

tym = 玩家('tym')
tym.金币 = 37
tym.角色 = '花一番玉虚总菊五雷大真人玄都境万寿帝君'
tym.英雄池 = []
tym.手牌 = 6
tym.积分 = 0

sxd = 玩家('sxd')
sxd.金币 = 9
sxd.角色 = '潜伏'
sxd.英雄池 = ['轮子妈', '盖伦']
sxd.手牌 = 2
sxd.积分 = 8

zhl = 玩家('zhl')
zhl.金币 = 2
zhl.角色 = 'KoKou'
zhl.英雄池 = ['霞', '泰坦', '机器人']
zhl.手牌 = 0
zhl.积分 = 18

cbt = 玩家('cbt')
cbt.金币 = 8
cbt.角色 = '穿山甲'
cbt.英雄池 = ['火男', '吸血鬼', '锤石']
cbt.手牌 = 0
cbt.积分 = 26

游戏.玩家列表.append(zer)
游戏.玩家列表.append(xjb)
游戏.玩家列表.append(zxx)
游戏.玩家列表.append(pzk)
游戏.玩家列表.append(tym)
游戏.玩家列表.append(sxd)
游戏.玩家列表.append(zhl)
游戏.玩家列表.append(cbt)

游戏.控制 = ["猫", '盖伦', '猫', '泽拉斯', '卡特', '轮子妈']
'''
print("\033[31m这是红色字体\033[0m")
print("\033[32m这是绿色字体\033[0m")
print("\033[33m这是黄色字体\033[0m")
print("\033[34m这是蓝色字体\033[0m")
print("\033[38m这是默认字体\033[0m")
print("\033[7m这是默认红色字体背景绿色\033[0m")
'''
网络.start()
# 网络.套接字.connect(('127.0.0.1', 8888))
# 网络.套接字.connect(('122.244.121.51', 8888))

listen()
# 开始监听键盘
# 开始监听网络

while True:
    action = random.randint(1, 3)
    player = 游戏.玩家列表[random.randint(0, 7)]
    if action == 1:
        游戏.消息队列.append(f"{player.ID} 已获得2金")
        游戏.玩家列表.搜索(player.ID).金币 += 2
    elif action == 2:
        游戏.消息队列.append(f"{player.ID} 已获得1手牌")
        游戏.玩家列表.搜索(player.ID).手牌 += 1
    elif action == 3:
        if 游戏.玩家列表.搜索(player.ID).金币 >= 6:
            游戏.玩家列表.搜索(player.ID).金币 -= 6
            游戏.玩家列表.搜索(player.ID).积分 += 6
            游戏.玩家列表.搜索(player.ID).英雄池.append('猫')
            游戏.消息队列.append(f"{player.ID} 花费 6 金，装备了【猫】")
        else:
            游戏.消息队列.append(f"{player.ID} 想花费 6 金装备【猫】，但是他没有钱！")
    time.sleep(1)
    UI.refresh()


'''
version = '1.15'
client = 网络()
client.start()
'''
