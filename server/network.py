import os
import json
import threading
import socket


class Admin:
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
                    print('[Server] 无法解析json数据包:', self.connection.getsockname(), self.connection.fileno())
                    print(obj)
            except ConnectionResetError:
                print('[Server] 连接失效:', self.connection.getsockname(), self.connection.fileno())
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

        # 下面的用于

    def 登录(self, 用户名, 密码):
        # self.login_username = input("输入用户名：")
        # self.login_password = input("输入密码： ")
        self.用户名 = 用户名
        self.密码 = 密码

        try:
            print(f"正在尝试登录: {self.用户名}")
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

    def 注册(self, login_username, login_password):
        # 记得在客户端上 要他再输入一次
        if os.path.exists(f'./usr/{login_username}'):
            print("用户名已存在")
        else:
            self.文件 = open(f"./usr/{login_username}", mode='w', encoding='cp936')
            self.文件.write(f"PW = {login_password}\nGD = 0\nDQ = 0\nWM = 0\nLM = 0\n\n")
            print("注册成功！")
            self.文件.close()

    def receive(self):
        self.连接.listen()

    def send(self, message):
        self.连接.send((json.dumps({
                    'type': 'update',
                    'message': message,
                }).encode()))

    def logout(self):
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


class 服务器:
    套接字 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @classmethod
    def __user_thread(cls, user_id):
        """
        用户子线程
        :param user_id: 用户id
        """
        connection = None

        # 侦听
        while True:
            # noinspection PyBroadException
            fuffer = ''
            try:
                # 解决断包问题
                while True:
                    # time.sleep(0.1)
                    buffer = cls.套接字.recv(1024).decode()
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
                print('无法从客户端获取数据')
                return
            # except OSError:
            except json.decoder.JSONDecodeError:
                # print(f"\n\n\nfuffer\n\n\n")
                # print(f'obj = {obj}')
                if fuffer == '':
                    print('\n可能是服务器关闭或BUG，无法接收信息。')
                else:
                    print(f'\n{fuffer}\n')
                    print('可能是黏包问题，解码失败，无法显示这句话。')
            '''
            try:
                buffer = connection.recv(1024).decode()
                # 解析成json数据
                obj = json.loads(buffer)
                # 如果是广播指令
                if True:
                    pass
                else:
                    print('[Server] 无法解析json数据包:', connection.getsockname(), connection.fileno())
            except Exception:
                print('[Server] 连接失效:', connection.getsockname(), connection.fileno())
            '''

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
            print('收到一个新连接', 连接.getsockname(), 连接.fileno())
            # try:
            while True:
                缓存 = 连接.recv(1024).decode()
                # 解析成json数据
                对象 = json.loads(缓存)
                print(对象)


            # except Exception:
            #     print('[Server] 无法接受数据:', connection.getsockname(), connection.fileno())
            #     print(obj)


class PlayerController:
    '''
    这个类用于管理Player，包括客户端连接、存储用户数据、玩家行为
    '''

    admin = Admin()
    player_list = list()

    @classmethod
    def connect(cls, login_username, login_password):  # 传入 username 和 password，交给 Player.login 去验证
        # 现在的逻辑是，新连进来的客户端先被这个函数安排一个位置，然后再进行登录操作，登录成功后再检测是否这次登录和以前的有重名
        # 如果有，那就把这次的放到那里去并且把那个删掉
        # if found someone connected
        # self.player_online.append(Player())
        cls.player_list.append(玩家())  # 加一个位置
        if cls.player_list[len(cls.player_list) - 1].登录(login_username=login_username, login_password=login_password) == 0:  # 先给连进来的新客户端分个位置
            print(f"连接成功 {cls.player_list[len(cls.player_list) - 1].login_username}")
        else:
            print("连接失败")
            return 1

        # 如果他的名字和某一个一样 那就证明要不就重复登录 要不就重连
        x = 0
        for player in cls.player_list:
            if cls.player_list[len(cls.player_list) - 1].login_username == player.login_username and x != len(cls.player_list) - 1 and player.exist:
                cls.disconnect(player.login_username)  # 因为先进来的排在前面，肯定会被先搜到，所以这样写没关系
                print(f"他的登录顶替了原来这个账号在player_list中的位置！")
                cls.player_list.insert(x, cls.player_list[-1])
                del cls.player_list[x + 1]
                del cls.player_list[-1]
            x += 1
        return 0

    @classmethod
    def disconnect(cls, player_name):
        cls.player_list[cls.find(player_name)].logout()
        cls.player_list[cls.find(player_name)].online = False
        # if found someone disconnected numbered x
        # del player_online[0]

    @classmethod
    def find(cls, name):
        x = 0
        for player in cls.player_list:
            if player.login_username == name:
                return x
            x += 1
        return -1


