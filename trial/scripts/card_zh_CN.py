from scripts.characters_zh_CN import *
import random


class 卡牌:
    价值 = 0
    加成 = list()

    def __init__(self):
        self.价值 = 0
        self.加成 = list()

    def 学习(self):
        self.加成.append('CBT')
    # 这个好像没有用？？

    def 购买(self, 对象):
        if 对象.金币 >= self.价值:
            对象.金币 -= self.价值
            对象.英雄池.append(self)
            对象.手牌.remove(self)
            return 0
        else:
            return -1

    def 被拆(self, 对象, 弃牌堆):
        弃牌堆 = 牌堆类()
        对象.英雄池.remove(self)
        弃牌堆.append(self)

    def 判断加成(self, 角色):
        for 临时 in self.加成:
            if 角色.缩写 == 临时:
                return True
        return False


class 泽拉斯(卡牌):
    def __init__(self):
        super().__init__()
        self.价值 = 14
        self.加成 = ['XJB']

    def 技能(self, 变量, 对象):
        if 对象.角色.缩写 == 'XJB':
            # 变量 == 1 时启动，变量 == 0 时释放
            if 变量 == 1:
                对象.积分 += 100
            if 变量 == 0:
                对象.积分 -= 100


class 牌堆类(list):
    def 初始化(self):
        self.append(卡牌())
        self.洗牌()

    def 洗牌(self):
        random.shuffle(self)


class 游戏:
    def __init__(self, 玩家列表):
        self.玩家列表 = 玩家列表
        random.shuffle(玩家列表)
        角色池 = [我是俊博之王(), 德思勤六楼的工头(), Sparrow(), 昊天金阙无上至尊自然秒有弥罗至真玉皇上帝(), 花一番玉虚总菊五雷大真人玄都境万寿帝君(), 痞子(), 穿山甲(), 陈伯伯(), 长方体移动师(), KoKou()]
        牌堆 = 牌堆类()
        弃牌堆 = 牌堆类()
        牌堆.初始化()

    def 开始(self):
        self.玩家列表[0].角色 = 花一番玉虚总菊五雷大真人玄都境万寿帝君()
        self.玩家列表[0].金币 += 100
        self.玩家列表[0].手牌.append(泽拉斯())
        self.玩家列表[0].手牌[0].购买(self.玩家列表[0])
        self.玩家列表[0].英雄池[0].技能(1, self.玩家列表[0])
        print(self.玩家列表[0].积分)



class 玩家:
    def __init__(self):
        self.金币 = 0
        self.角色 = None
        self.英雄池 = list()
        self.手牌 = list()
        self.积分 = 0

    def 拿牌(self, 牌堆, 弃牌堆):
        if len(牌堆) <= 1:
            print("牌堆剩余牌数不够，正在对弃牌堆洗牌")
            牌堆 += 弃牌堆
            牌堆.洗牌()
            if len(牌堆) <= 1:
                print('洗牌后牌堆牌数仍不够，已自动转为获得2金')
                self.金币 += 2
                print(self.金币)
        print(f"{牌堆[0]}, {牌堆[1]}")


a = 游戏([玩家(), 玩家(), 玩家()])
a.开始()


"""
    global paidui
    global qipaidui
    global shoupai
    if paidui == []:
        printb('[ERROR] 牌堆牌数不够，正在尝试洗牌')
        qipaidui += paidui
        paidui = recard(qipaidui)
    if paidui == []:
        printb('[ERROR] 洗牌后牌堆牌数仍不够，已自动转为获得2金')
        gold[player_to_get] += 2
        printb(f'金币 = {gold}')
        return
    print(translate_card(paidui))
    printp(f'''\n       1. {card[paidui[0]]}   和   2. {card[paidui[1]]}
            {card_cost[paidui[0]]}金                {card_cost[paidui[1]]}金
增益对象：    {champ[card_color[paidui[0]]]}            {champ[card_color[paidui[1]]]}\n''', player_to_get)
    '''
    {card_cost[paidui[0]]}金 和 {card_cost[paidui[1]]}金
增益对象：{champ[card_color[paidui[0]]]} 、{champ[card_color[paidui[1]]]}
    '''
    control = inputp(f'[INPUT]请从 1. {card[paidui[0]]} 和 2. {card[paidui[1]]} 中选择: ', player_to_get)
    if control == 1:
        print(f"shoupai[player_to_get] = {shoupai[player_to_get]}")
        shoupai[player_to_get].append(paidui[0])
        print(f"shoupai[player_to_get] = {shoupai[player_to_get]}")
        paidui.remove(paidui[0])
    elif control == 2:
        print(f"shoupai[player_to_get] = {shoupai[player_to_get]}")
        shoupai[player_to_get].append(paidui[1])
        print(f"shoupai[player_to_get] = {shoupai[player_to_get]}")
        paidui.remove(paidui[1])
    paidui.append(paidui[0])
    paidui.remove(paidui[0])
"""