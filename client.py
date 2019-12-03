# -*- coding: cp936 -*-
import operator
import socket
import threading
import json
import os
import time
import random

宽度 = 64
高度 = 65

os.system('title 监狱威龙客户端（控制台版）')
os.system(f'MODE con: COLS={宽度} LINES={高度}')


class UI:
    """UI类负责所有的（文字版本的）UI绘制"""
    垂直同步 = True
    if 垂直同步:
        总输出 = ''

    @classmethod
    def printc(cls, 内容):  # 全局控制居中输出，只要垂直同步是True 就会保存到总输出里
        global 宽度
        汉字计数 = 0
        总共计数 = 0
        输出 = ''
        for 字 in 内容:
            if '\u4e00' <= 字 <= '\u9fa5':
                汉字计数 += 1
            总共计数 += 1
        空格数 = 宽度 // 2 - 总共计数 // 2 - 汉字计数 // 2
        if 空格数 < 0:
            空格数 = 0
        输出 = ' ' * 空格数 + 内容
        if cls.垂直同步:
            if 内容 == '\n':
                cls.总输出 += '\n'
            else:
                cls.总输出 += 输出 + '\n'
        else:
            if 内容 == '\n':
                print()
            else:
                print(输出)

    @staticmethod
    def 翻译英雄池(列表):  # 打印列表
        if not 列表:
            return '无'
        字符串 = ''
        for 英雄 in 列表:
            字符串 += f'{英雄} '
        return 字符串

    '''
    @classmethod
    def __print(cls, 内容):  # 复写print来达到控制垂直同步的目的
        if cls.垂直同步:
            cls.总输出 += 内容 + '\n'
        else:
            print(内容)
    '''

    @staticmethod
    def cls():
        os.system('cls')

    @classmethod
    def draw_line(cls, number=None, ID = None):
        if number and ID:
            cls.printc(f"-- {number} {ID} --")
        else:
            cls.printc("  ---------------------------------------------------  ")

    @classmethod
    def draw_rank(cls, 游戏):
        rank = 1
        cls.draw_line()
        # cls.printc("排行榜")
        # cls.draw_line()
        # cls.draw_line()
        for 玩家 in 游戏.玩家列表:
            cls.draw_line(number=rank, ID=玩家.ID)
            cls.printc(f"【{玩家.角色}】")
            # print(' ' * 10 + str(玩家.角色))
            cls.printc(f"{玩家.金币}金币" + ' ' * 3 + \
                       f"{玩家.手牌}手牌" + ' ' * 3 + str(玩家.积分) + '积分')
            cls.printc(cls.翻译英雄池(玩家.英雄池))
            if rank != len(游戏.玩家列表):
                cls.printc('\n')
            rank += 1

    @classmethod
    def draw_message(cls, 游戏):
        cls.draw_line()
        # cls.printc("通告栏")
        # cls.draw_line()
        条数 = 10
        while len(游戏.消息队列) > 条数:
            del 游戏.消息队列[0]
        for 消息 in 游戏.消息队列:
            cls.printc(消息)
        if len(游戏.消息队列) < 条数:
            for i in range(1, 条数 + 1 - len(游戏.消息队列)):
                cls.printc('\n')

    @classmethod
    def draw_card(cls, 游戏):
        pass

    @classmethod
    def draw_round(cls, 游戏):
        cls.printc(f"第{游戏.回合}回合")

    @classmethod
    def draw_control(cls, 游戏):
        cls.draw_line()
        # cls.printc("手牌区")
        # cls.draw_line()
        cls.draw_card(游戏.手牌)

    @classmethod
    def refresh(cls, 游戏):
        cls.cls()
        cls.draw_round(游戏)
        cls.draw_message(游戏)
        cls.draw_rank(游戏)
        cls.draw_control(游戏)
        if cls.垂直同步:
            print(cls.总输出)
            cls.总输出 = ''


class 玩家:
    def __init__(self, ID):
        self.ID = ID
        self.金币 = 0
        self.角色 = None  # None = 未公布
        self.英雄池 = list()
        self.手牌 = None  # 对于别的玩家，只能看到手牌数但是不能看到几张牌
        self.积分 = 0


class Client:
    """
    客户端
    """

    def __init__(self):
        """
        构造
        """
        super().__init__()
        self.god = False
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__id = None
        self.__nickname = None

    def __receive_message_thread(self):
        """
        接受消息线程
        """
        while True:
            # noinspection PyBroadException
            try:
                fuffer = ''

                # 解决断包问题
                while True:
                    # time.sleep(0.1)
                    buffer = self.__socket.recv(1024).decode()
                    fuffer += buffer
                    if buffer == '' or buffer[-1] == '}':
                        break

                # 解决黏包问题
                find = 0
                # print(type(fuffer))
                # print(f"fuffer = {fuffer}")
                fuffer_split = []
                while find < len(fuffer) - 1:
                    if fuffer[find] == "}" and fuffer[find + 1] == "{":
                        fuffer_split.append(fuffer[0:find + 1])  # 注意：包括开头，不包括结尾！
                        fuffer = fuffer[find + 1:]
                        find = -1
                    find += 1
                # print(f"current fuffer = {fuffer}")
                fuffer_split.append(fuffer)
                if fuffer_split:
                    # print(f"fuffer_split = {fuffer_split}\n")
                    for item in fuffer_split:
                        obj = json.loads(item)
                        print(f"{obj}")
                    # fuffer_split.clear()
                else:
                    obj = json.loads(fuffer)
                    print(f"{obj}")
                # 这里重复了代码。记得改。
            except OSError:
                print('无法从服务器获取数据')
                return
            # except OSError:
            except json.decoder.JSONDecodeError:
                # print(f"\n\n\nfuffer\n\n\n")
                # print(f'obj = {obj}')
                if fuffer == '':
                    print('\n可能是服务器关闭或BUG，无法接收信息。')
                    time.sleep(30)
                else:
                    print(f'\n{fuffer}\n')
                    print('可能是黏包问题，解码失败，无法显示这句话。')

            """
            原始
                    while True:
            fuffer = ''
            # noinspection PyBroadException
            try:
                # 解决断包问题
                while True:
                    buffer = self.__socket.recv(1024).decode()
                    fuffer += buffer
                    if buffer == '':
                        break
                    if buffer[-1] == '}':
                        break

                # 解决黏包问题
                find = 0
                fuffer_split = []
                while find < len(fuffer) - 1:
                    if fuffer[find] == "}" and fuffer[find + 1] == '{':
                        fuffer_split.append(fuffer[0:find + 1])  # 注意：包括开头，不包括结尾！
                        fuffer = fuffer[find + 1:0]
                        find = 0
                    find += 1
                if fuffer_split:
                    for item in fuffer_split:
                        obj = json.loads(item)
                        print(obj)
                else:
                    obj = json.loads(fuffer)
                    print(obj)
                # 这里重复了代码。记得改。

            except OSError:
                print('无法从服务器获取数据')
                return
            # except OSError:
            except json.decoder.JSONDecodeError:
                # print(f"\n\n\nfuffer\n\n\n")
                # print(f'obj = {obj}')
                if fuffer == '':
                    print('\n可能是服务器关闭或BUG，无法接收信息。')
                    time.sleep(30)
                else:
                    print(f'\n{fuffer}\n')
                    print('可能是黏包问题，解码失败，无法显示这句话。')
            """

            """
            # 没有解决粘包断包问题的版本
            try:
                buffer = self.__socket.recv(1024).decode()
                obj = json.loads(buffer)
                print(obj)
                # 这里重复了代码。记得改。
            except OSError:
                print('无法从服务器获取数据')
                return
                # except OSError:
            except json.decoder.JSONDecodeError:
                print(f"解码失败, buffer = {buffer}, obj = {obj}")
            # print(f"\n\n\nfuffer\n\n\n")
            # print(f'obj = {obj}')
            """

    def __send_message_thread(self, type, message):
        """
        发送消息线程
        :param message: 消息内容
        """
        if self.god is True:
            temp = message.split(" ")
            try:
                self.__socket.send(json.dumps({
                    'type': 'change',
                    'username': temp[0],
                    'thing': temp[1],
                    'add': temp[2]
                }).encode())
            except IndexError:
                print("缺少数据")
        else:
            self.__socket.send(json.dumps({
                'type': type,
                'message': message
            }).encode())
        '''
print(f"""抱歉，你的版本过低，服务器已断开与你的连接。
服务器版本：{obj['version']}，你的版本：{version}。
请联系开发者获得最新版本。""")'''

    '''
        self.__socket.send(json.dumps({
            # 'type': 'broadcast',
            'type': 'broadcast',
            'sender_id': self.__id,
            'message': message
        }).encode())
    '''

    def do_login(self):
        """
        登录聊天室
        :param args: 参数
        """
        global version
        username = input("用户名：")
        # password = input("密码：")
        password = 1
        # 将昵称发送给服务器，获取用户id
        self.__socket.send(json.dumps({
            'type': 'login',
            'username': username,
            'password': password,
            'version': version,
        }).encode())
        # 尝试接受数据
        # noinspection PyBroadException
        try:
            # buffer = self.__socket.recv(1024).decode()
            # obj = json.loads(buffer)
            # clear()
            # print(f'登录请求已发送：【{obj}】')
            # 开启子线程用于接受数据
            thread = threading.Thread(target=self.__receive_message_thread)
            thread.setDaemon(True)
            thread.start()
        except json.decoder.JSONDecodeError:
            print('解码错误，{obj}')
        except KeyError:
            clear()
            print(f'请更新版本。\n当前客户端版本：{version}\n服务器版本：{obj["version"]}')
            exit()

    def do_send(self, args):
        """
        发送消息
        :param args: 参数
        """
        message = args
        # 开启子线程用于发送数据
        thread = threading.Thread(target=self.__send_message_thread, args=(message,))
        thread.setDaemon(True)
        thread.start()

    def start(self):
        global version
        """
        启动客户端
        """
        try:
            print(f'监狱威龙 客户端\n\n版本：{version}。\n\n')
            self.__socket.connect(('127.0.0.1', 8888))
            # self.__socket.connect(('47.98.179.115', 34674))
            print('正在尝试登录。\n')
            self.do_login()
        except ConnectionRefusedError:
            print('本地服务器未开启！请联系开发者。')
        while True:
            self.do_send(input())


class 游戏:
    class 玩家列表类(list):
        def __init__(self, *args):
            super().__init__(*args)

        def 搜索(self, ID):
            for 玩家 in self:
                # print(玩家.ID)
                if 玩家.ID == ID:
                    return 玩家
    房间名 = '' + '的房间'
    玩家列表 = 玩家列表类()
    消息队列 = list()
    输入 = None
    控制 = None
    手牌 = list()
    回合 = 1


'''
    def 改值(self, 玩家, 信息, 修改量):  # 肯定根据ID来搜啊 你这傻逼
        self.玩家列表[a.玩家列表.index(pzk)].金币 += 2
        '''

a = 游戏()

a.消息队列 = ["现在轮到选择 长方体移动师 的玩家行动！", "选择 长方体移动师 的玩家是 pzk ！", "pzk 正在选择获得手牌或者金币"]

xjb = 玩家('xjb')
xjb.金币 = 10
xjb.角色 = '昊天金阙无上至尊自然妙有弥罗至真玉皇上帝'
xjb.英雄池 = ['泽拉斯', '狐狸', '盖伦']
xjb.手牌 = 1
xjb.积分 = 20

zer = 玩家('zer')
zer.金币 = 7
zer.角色 = '潜伏'
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
tym.角色 = '潜伏'
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
cbt.角色 = '潜伏'
cbt.英雄池 = ['火男', '吸血鬼', '锤石']
cbt.手牌 = 0
cbt.积分 = 26

a.玩家列表.append(zer)
a.玩家列表.append(xjb)
a.玩家列表.append(zxx)
a.玩家列表.append(pzk)
a.玩家列表.append(tym)
a.玩家列表.append(sxd)
a.玩家列表.append(zhl)
a.玩家列表.append(cbt)

cmpfun = operator.attrgetter('积分')
a.玩家列表.sort(key=cmpfun, reverse=True)


a.控制 = "你现在可以使用一张手牌"
'''
print("\033[31m这是红色字体\033[0m")
print("\033[32m这是绿色字体\033[0m")
print("\033[33m这是黄色字体\033[0m")
print("\033[34m这是蓝色字体\033[0m")
print("\033[38m这是默认字体\033[0m")
print("\033[7m这是默认红色字体背景绿色\033[0m")
'''

while True:
    index = random.randint(1, 3)
    if index == 1:
        a.消息队列.append("pzk 已获得2金")
        a.玩家列表.搜索('pzk').金币 += 2
    elif index == 2:
        a.消息队列.append("pzk 正在使用技能")
    elif index == 3:
        a.玩家列表.搜索('pzk').金币 -= 13
        a.消息队列.append("pzk 花费 13 金，拆掉了 xjb 的 泽拉斯！")
    UI.refresh(游戏=a)
    time.sleep(0.5)

version = '1.15'

time.sleep(100)

# client = Client()
# client.start()
