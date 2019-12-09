# -*- coding: utf-8 -*-

import os
import json
import threading
import socket


class 管理员:
    def __init__(self):
        global p
        self.connection = None
        self.temp = None

    def listen(self):
        # 侦听
        while True:
            # noinspection PyBroadException
            try:
                buffer = self.connection.recv(1024).decode()
                # 解析成json数据
                obj = json.loads(buffer)
                # 如果是广播指令
                if obj['type'] == 'change':
                    self.change(username=obj['username'], thing=obj['thing'], add=int(obj['add']))
                else:
                    print('[Server] 无法解析json数据包:', self.connection.getpeername(), self.connection.fileno())
                    print(obj)
            except ConnectionResetError:
                print('[Server] 连接失效:', self.connection.getpeername(), self.connection.fileno())
                break
            except IndexError:
                print('输错了，没有起到作用')
                self.connection.send(json.dumps({
                    "message": "没有起到作用"
                }))

            # 但是现在就必须要那个用户登录了才可以

    def change(self, username, thing, add):
        global p
        pass

    def read(self):
        pass

    def online(self):
        pass


class 玩家:
    def __init__(self):

        # 下面的用于login
        self.用户名 = None  # 登陆时使用的用户名
        self.密码 = None  # 登陆时使用的密码
        self.文件 = None  # 读取的用户文件
        self.在线 = False  # 是否登陆成功
        self.金币 = 0  # 金币
        self.点券 = 0  # 点券
        self.胜场 = 0  # 胜场
        self.负场 = 0  # 负场
        self.房间 = -1  # 游戏房间号 -1为在大厅
        self.游戏中 = False  # 游戏中
        self.exist = False
        self.连接 = None
        self.IP = None

    def 登录(self, 用户名, 密码):
        self.用户名 = 用户名
        self.密码 = 密码
        '''
        try:
            self.文件 = open(f"./usr/{self.用户名}", "r", encoding='utf-8')  # 我的Windows 用的是cp936 不是 UTF-8
            self.exist = True

            for 行 in self.文件:
                if 行[0:5] == "PW = ":
                    if self.密码 == 行[5:-1]:  # line[5:-1] 就是密码，-1 的原因是要去掉\n
                        if self.在线:
                            print("你把这个号上正在线的玩家踢下线了！！")
                        print(f"登录成功！欢迎 {self.用户名}")
                        self.在线 = True
                        if self.房间 is True:
                            print("你正在参与一场游戏，正在重连")
                            self.reconnect(self)
                    else:
                        print(f"登录失败：密码错误")
                        self.在线 = False
                        return 1
                elif 行[0:5] == "GD = ":
                    self.金币 = int(行[5:-1])
                elif 行[0:5] == "DQ = ":
                    self.点券 = int(行[5:-1])
                elif 行[0:5] == "WM = ":
                    self.胜场 = int(行[5:-1])
                elif 行[0:5] == "LM = ":
                    self.负场 = int(行[5:-1])
            print(f"拥有金币：{self.金币}\n"
                  f"拥有点券：{self.点券}\n"
                  f"胜场：{self.胜场}\n"
                  f"负场：{self.负场}\n")
            try:
                print(f"胜率：{'{:.2%}'.format(self.胜场 / (self.胜场 + self.负场))}\n")
            except ZeroDivisionError:
                print(f"胜率：0.00%")
            # 关闭打开的文件
            self.文件.close()
            return 0
        except OSError:
            print('在数据库中没有这个玩家')
            return 1
        '''
        self.在线 = True
        self.连接.send(json.dumps({
            '类型': '登录',
            '数据': '登录成功',
        }).encode())

    def 注册(self, login_username, login_password):
        # 记得在客户端上 要他再输入一次
        if os.path.exists(f'./usr/{login_username}'):
            print("用户名已存在")
        else:
            self.文件 = open(f"./usr/{login_username}", mode='w', encoding='cp936')
            self.文件.write(f"PW = {login_password}\nGD = 0\nDQ = 0\nWM = 0\nLM = 0\n\n")
            print("注册成功！")
            self.文件.close()

    def 接收(self):
        self.连接.listen()

    def 发送(self, message):
        self.连接.send((json.dumps({
                    'type': 'update',
                    'message': message,
                }).encode()))

    def 登出(self):
        try:
            self.文件 = open(f"./usr/{self.用户名}", "w+", encoding='cp936')
            print(f"正在登出: {self.用户名}")
            self.文件.write(f"PW = {self.密码}\n"
                         f"GD = {self.金币}\n"
                         f"DQ = {self.点券}\n"
                         f"WM = {self.胜场}\n"
                         f"LM = {self.负场}\n\n")
            print("登出成功，文件已写入，再见")
            # 关闭打开的文件
            self.文件.close()
            return 0
        except AttributeError:
            print('在数据库中没有这个玩家！')
            return 1

    @staticmethod
    def reconnect(self):
        print("重连成功")
        pass

    def 处理信息(self, obj):
        if obj['type'] == '出牌':
            pass


class 服务器:
    套接字 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @classmethod
    def 用户线程(cls, 连接):
        # 侦听
        while True:
            全缓存 = ''
            try:
                # 解决断包问题
                while True:
                    缓存 = 连接.recv(1024).decode()
                    全缓存 += 缓存
                    if 缓存 == '' or 缓存[-1] == '}':
                        break

                # 解决黏包问题
                指针 = 0
                # print(type(全缓存))
                # print(f"全缓存 = {全缓存}")
                全缓存分割 = list()
                while 指针 < len(全缓存) - 1:
                    if 全缓存[指针] == "}" and 全缓存[指针 + 1] == "{":
                        全缓存分割.append(全缓存[0:指针 + 1])  # 注意：包括开头，不包括结尾！
                        全缓存 = 全缓存[指针 + 1:]
                        指针 = -1
                    指针 += 1
                # print(f"current 全缓存 = {全缓存}")
                全缓存分割.append(全缓存)
                if 全缓存分割:
                    # print(f"全缓存分割 = {全缓存分割}\n")
                    for item in 全缓存分割:
                        obj = json.loads(item)
                        print(f"来自 {连接.getpeername()} 的消息：{obj}")
                        # 玩家.处理信息(obj)
                    全缓存分割.clear()
                else:
                    obj = json.loads(全缓存)
                    print(f"来自 {连接.getpeername()} 的消息：{obj}")
                # 这里重复了代码。记得改。
            except OSError:
                print(f"{连接.getpeername()} 的连接已断开。")
                return
            # except OSError:
            except json.decoder.JSONDecodeError:
                # print(f"\n\n\nfuffer\n\n\n")
                # print(f'obj = {obj}')
                if 全缓存 == '':
                    print('\n可能是服务器关闭或BUG，无法接收信息。')
                else:
                    print(f'\n{全缓存}\n')
                    print('可能是黏包问题，解码失败，无法显示这句话。')

    @classmethod
    def 启动(cls):
        """
        启动服务器
        """
        # 绑定端口
        cls.套接字.bind(('127.0.0.1', 8888))

        # 启用监听
        cls.套接字.listen(5)
        print('服务器已启动，等待连接')

        # 开始侦听
        while True:
            连接, 地址 = cls.套接字.accept()
            print('收到一个新连接', 连接.getpeername(), 连接.fileno())

            线程 = threading.Thread(target=cls.用户线程(连接))
            线程.start()
            # 线程 = threading.Thread(target=cls.用户线程(连接))
            # 线程.start()


class 玩家控制:
    '''
    这个类用于管理Player，包括客户端连接、存储用户数据、玩家行为
    '''

    玩家列表 = list()

    @classmethod
    def 登录(cls, 用户名, 密码=100):  # 传入 username 和 password，交给 Player.login 去验证
        # 现在的逻辑是，新连进来的客户端先被这个函数安排一个位置，然后再进行登录操作，登录成功后再检测是否这次登录和以前的有重名
        # 如果有，那就把这次的放到那里去并且把那个删掉
        cls.玩家列表.append(玩家())  # 加一个位置
        '''
        if cls.玩家列表[-1].登录(用户名, 密码) == 0:  # 先给连进来的新客户端分个位置
            print(f"连接成功 {cls.玩家列表[len(cls.玩家列表) - 1].用户名}")
        else:
            print("连接失败")
            return 1
        # 先不用密码 就登陆上就ok
        '''
        cls.玩家列表[-1].登录(用户名, 密码)

        # 如果他的名字和某一个一样 那就证明要不就重复登录 要不就重连
        x = 0
        for 对象 in cls.玩家列表:
            if cls.玩家列表[-1].用户名 == 对象.用户名 and x != len(cls.玩家列表) - 1 and 对象.exist:
                cls.断开(对象.用户名)  # 因为先进来的排在前面，肯定会被先搜到，所以这样写没关系
                print(f"他的登录顶替了原来这个账号在player_list中的位置！")
                cls.玩家列表.insert(x, cls.玩家列表[-1])
                del cls.玩家列表[x + 1]
                del cls.玩家列表[-1]
            x += 1
        return 0

    @classmethod
    def 断开(cls, player_name):
        cls.寻找(player_name).登出()
        cls.寻找(player_name).在线 = False
        # if found someone disconnected numbered x
        # del player_online[0]

    @classmethod
    def 寻找(cls, ID):
        x = 0
        for 对象 in cls.玩家列表:
            if 对象.用户名 == ID:
                return 对象
            x += 1
        return -1

'''
# 不能这样做，因为./usr/这个文件夹不在这里！
if __name__ == '__main__':
    玩家控制.connect('nihao', 'nihao')
'''
