from scripts.characters_zh_CN import *
import random
import json
import socket
import time


class 卡牌:
    价值 = 0
    加成 = list()

    def __init__(self):
        self.价值 = 0
        self.加成 = list()

    '''
        def 学习(self):
        self.加成.append('CBT')
        # 这个好像没有用？？
    '''

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
        self.append(泽拉斯())
        self.append(泽拉斯())
        self.append(泽拉斯())
        self.append(泽拉斯())
        self.洗牌()

    def 洗牌(self):
        random.shuffle(self)


class 角色池类(list):

    def 重置(self):
        self.clear()
        self.append(我是俊博之王())
        self.append(德思勤六楼的工头())
        self.append(Sparrow())
        self.append(昊天金阙无上至尊自然妙有弥罗至真玉皇上帝())
        self.append(花一番玉虚总菊五雷大真人玄都境万寿帝君())
        self.append(痞子())
        self.append(穿山甲())
        self.append(陈伯伯())
        self.append(长方体移动师())
        self.append(KoKou())


class 游戏:
    玩家列表 = []

    def __init__(self, 玩家列表=玩家列表):
        self.玩家列表 = 玩家列表
        random.shuffle(玩家列表)
        self.角色池 = 角色池类()
        self.牌堆 = 牌堆类()
        self.弃牌堆 = 牌堆类()
        self.牌堆.初始化()

    def 开始(self):
        '''
        self.玩家列表[0].角色 = 花一番玉虚总菊五雷大真人玄都境万寿帝君()
        self.玩家列表[0].金币 += 100
        self.玩家列表[0].手牌.append(泽拉斯())
        self.玩家列表[0].手牌[0].购买(self.玩家列表[0])
        self.玩家列表[0].英雄池[0].技能(1, self.玩家列表[0])
        self.广播(self.玩家列表[0].积分)
        self.玩家列表[0].拿牌(self.牌堆, self.弃牌堆)
        '''
        random.shuffle(self.玩家列表)
        self.角色池.重置()
        random.shuffle(self.角色池)
        联网.广播(玩家列表=self.玩家列表, 信息='游戏开始了！')
        for 玩家 in self.玩家列表:
            玩家.角色 = self.角色池.pop()
            联网.私发(对象=玩家, 信息=f'你第一轮分到的角色是 {玩家.角色.名字} ！')


class 玩家:
    def __init__(self, ID):
        self.ID = ID
        self.金币 = 0
        self.角色 = None
        self.英雄池 = list()
        self.手牌 = list()
        self.积分 = 0
        self.连接 = None
        self.回应 = None

    def 拿牌(self, 游戏):
        if len(游戏.牌堆) <= 1:
            print("牌堆剩余牌数不够，正在对弃牌堆洗牌")
            游戏.牌堆 += 游戏.弃牌堆
            游戏.牌堆.洗牌()
            if len(游戏.牌堆) <= 1:
                print('洗牌后牌堆牌数仍不够，已自动转为获得2金')
                self.金币 += 2
                print(self.金币)
        print(f"{游戏.牌堆[0]}, {游戏.牌堆[1]}")


class 联网:
    global a
    __人数变量 = 0
    __socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @classmethod
    def 开始(cls):
        """
        启动服务器
        """
        # 绑定端口
        cls.__socket.bind(('127.0.0.1', 8888))

        # 启用监听
        cls.__socket.listen(5)
        print('服务器已启动')

        # 开始侦听
        while True:
            连接, address = cls.__socket.accept()
            print('[Server] 收到一个新连接', 连接.getsockname(), 连接.fileno())

            # 尝试接受数据
            # noinspection PyBroadException
            # try:
            缓存 = 连接.recv(1024).decode()
            # 解析成json数据
            对象 = json.loads(缓存)
            # 如果是连接指令，那么则返回一个新的用户编号，接收用户连接
            if 对象['type'] == 'login':
                a.玩家列表.append(玩家(ID=对象['username']))
                a.玩家列表[-1].连接 = 连接
                cls.私发(a.玩家列表[-1], "登陆成功", "聊天", 对象['username'])
                '''
                a.玩家列表[cls.__人数变量].连接.send(json.dumps({
                    'message': f"连接成功，你现在是玩家{cls.__人数变量}"
                }).encode())
                '''
                cls.__人数变量 += 1
            if cls.__人数变量 == 4:
                cls.广播(玩家列表=a.玩家列表, 信息='已满4人，请准备！全员准备后游戏即将开始', 类型='notification', 玩家=None)
                a.开始()

    @classmethod
    def 广播(cls, 玩家列表=None, 信息='', 类型=None, 玩家=None):
        if 玩家列表 is None:
            玩家列表 = []
        for 对象 in 玩家列表:
            对象.连接.send(json.dumps({
                'type': 类型,
                'message': 信息,
                'player': 玩家
                }).encode())
            print(f"联网内 广播：'type': {类型}, 'message': {信息}, 'player': {玩家} 给 {对象.ID}")
            # time.sleep(0.001)  # 要是不加这一行就会有的数据收不到 我也不知道为什么

    @classmethod
    def 私发(cls, 对象=None, 信息='', 类型=None, 玩家=None):
        print(f"联网内 私发：'type': {类型}, 'message': {信息}, 'player': {玩家} 给 {对象.ID}")
        对象.连接.send(json.dumps({
                'type': 类型,
                'message': 信息,
                'player': 玩家
                }).encode())


a = 游戏()
联网.开始()

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