# 这是用来放 class Player 的文件！
import socket
import threading
import json
import os


class Server:
    """
    服务器类
    """
    def __init__(self):
        """
        构造
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connections = list()
        self.__nicknames = list()

    def __user_thread(self, user_id):
        """
        用户子线程
        :param user_id: 用户id
        """
        connection = self.__connections[user_id]
        nickname = self.__nicknames[user_id]
        print('[Server] 用户', user_id, nickname, '加入聊天室')
        self.__broadcast(message='用户 ' + str(nickname) + '(' + str(user_id) + ')' + '加入聊天室')

        # 侦听
        while True:
            # noinspection PyBroadException
            try:
                buffer = connection.recv(1024).decode()
                # 解析成json数据
                obj = json.loads(buffer)
                # 如果是广播指令
                if obj['type'] == 'broadcast':
                    self.__broadcast(obj['sender_id'], obj['message'])
                else:
                    print('[Server] 无法解析json数据包:', connection.getsockname(), connection.fileno())
            except Exception:
                print('[Server] 连接失效:', connection.getsockname(), connection.fileno())
                self.__connections[user_id].close()
                self.__connections[user_id] = None
                self.__nicknames[user_id] = None

    def __broadcast(self, user_id=0, message=''):
        """
        广播
        :param user_id: 用户id(0为系统)
        :param message: 广播内容
        """
        for i in range(1, len(self.__connections)):
            if user_id != i:
                self.__connections[i].send(json.dumps({
                    'sender_id': user_id,
                    'sender_nickname': self.__nicknames[user_id],
                    'message': message
                }).encode())

    def start(self):
        """
        启动服务器
        """
        # 绑定端口
        self.__socket.bind(('127.0.0.1', 8888))
        # 启用监听
        self.__socket.listen(10)
        print('服务器已启动')

        # 清空连接
        self.__connections.clear()
        self.__nicknames.clear()
        self.__connections.append(None)
        self.__nicknames.append('System')

        # 开始侦听
        while True:
            connection, address = self.__socket.accept()
            print('[Server] 收到一个新连接', connection.getsockname(), connection.fileno())

            # 尝试接受数据
            # noinspection PyBroadException
            try:
                buffer = connection.recv(1024).decode()
                # 解析成json数据
                obj = json.loads(buffer)
                # 如果是连接指令，那么则返回一个新的用户编号，接收用户连接
                if obj['type'] == 'login':
                    self.__connections.append(connection)
                    self.__nicknames.append(obj['nickname'])
                    connection.send(json.dumps({
                        'id': len(self.__connections) - 1
                    }).encode())

                    # 开辟一个新的线程
                    thread = threading.Thread(target=self.__user_thread, args=(len(self.__connections) - 1, ))
                    thread.setDaemon(True)
                    thread.start()
                else:
                    print('[Server] 无法解析json数据包:', connection.getsockname(), connection.fileno())
            except Exception:
                print('[Server] 无法接受数据:', connection.getsockname(), connection.fileno())


class Player:

    # 把所有在线的玩家放在一个 array 里，用 self.online 判断是否在线

    def __init__(self):

        # 下面的用于login
        self.login_username = None  # 登陆时使用的用户名
        self.login_password = None  # 登陆时使用的密码
        self.f = None  # 读取的用户文件
        self.online = False  # 是否登陆成功
        self.gold = 0  # 金币
        self.rp = 0  # 点券
        self.win_games = 0  # 胜场
        self.lose_games = 0  # 负场
        self.room = -1  # 游戏房间号 -1为在大厅
        self.playing = False  # 游戏中
        self.exist = False

        # 下面的用于

    def login(self, login_username, login_password):
        # self.login_username = input("输入用户名：")
        # self.login_password = input("输入密码： ")
        self.login_username = login_username
        self.login_password = login_password

        try:
            print(f"正在尝试登录: {self.login_username}")
            self.f = open(f"./usr/{self.login_username}", "r", encoding='cp936')  # 我的Windows 用的是cp936 不是 UTF-8
            self.exist = True

            for line in self.f:
                if line[0:5] == "PW = ":
                    if self.login_password == line[5:-1]:  # line[5:-1] 就是密码，-1 的原因是要去掉\n
                        if self.online:
                            print("你把这个号上正在线的玩家踢下线了！！")
                        print(f"登录成功！欢迎 {self.login_username}")
                        self.online = True
                        if self.room is True:
                            print("你正在参与一场游戏，正在重连")
                            self.reconnect()
                    else:
                        print(f"登录失败：密码错误")
                        self.online = False
                elif line[0:5] == "GD = ":
                    self.gold = int(line[5:-1])
                elif line[0:5] == "DQ = ":
                    self.rp = int(line[5:-1])
                elif line[0:5] == "WM = ":
                    self.win_games = int(line[5:-1])
                elif line[0:5] == "LM = ":
                    self.lose_games = int(line[5:-1])
            print(f"拥有金币：{self.gold}\n"
                  f"拥有点券：{self.rp}\n"
                  f"胜场：{self.win_games}\n"
                  f"负场：{self.lose_games}\n")
            try:
                print(f"胜率：{'{:.2%}'.format(self.win_games / (self.win_games + self.lose_games))}\n")
            except ZeroDivisionError:
                print(f"胜率：0.00%")
            # 关闭打开的文件
            self.f.close()
            return 0
        except OSError:
            print('在数据库中没有这个玩家')
            return 1

    def sign_up(self):
        self.login_username = input("输入你要注册的用户名：")
        self.login_password = input("输入你要注册的密码：")
        # 记得在客户端上 要他再输入一次
        if os.path.exists(f'./usr/{self.login_username}'):
            print("用户名已存在")
        else:
            self.f = open(f"./usr/{self.login_username}", mode='w', encoding='cp936')
            self.f.write(f"PW = {self.login_password}\nGD = 0\nDQ = 0\nWM = 0\nLM = 0\n\n")
            print("注册成功！")
            self.f.close()

    def logout(self):
        try:
            self.f = open(f"./usr/{self.login_username}", "w+", encoding='cp936')
            print(f"正在登出: {self.login_username}")
            self.f.write(f"PW = {self.login_password}\n"
                         f"GD = {self.gold}\n"
                         f"DQ = {self.rp}\n"
                         f"WM = {self.win_games}\n"
                         f"LM = {self.lose_games}\n\n")
            print("登出成功，文件已写入，再见")
            # 关闭打开的文件
            self.f.close()
            return 0
        except AttributeError:
            print('在数据库中没有这个玩家！')
            return 1

    @staticmethod
    def reconnect(self):
        print("重连成功")
        pass

# 按理来说应该谁登录谁就排在前面，有人下机就让他那个位置空出来给别人登录，只要一个客户端一连上服务器就给他先派一个位置


class PlayerController:
    # 我是传出还是传入？在谁那里操作？
    # 当有人进来时，用connect
    '''
    这个类用于管理Player，包括客户端连接、存储用户数据、玩家行为
    '''

    def __init__(self):
        self.player_list = []

    def connect(self, login_username, login_password):  # 传入 username 和 password，交给 Player.login 去验证
        # 现在的逻辑是，新连进来的客户端先被这个函数安排一个位置，然后再进行登录操作，登录成功后再检测是否这次登录和以前的有重名
        # 如果有，那就把这次的放到那里去并且把那个删掉
        # if found someone connected
        # self.player_online.append(Player())
        self.player_list.append(Player())  # 加一个位置
        if self.player_list[len(self.player_list) - 1].login(login_username=login_username, login_password=login_password) == 0:  # 先给连进来的新客户端分个位置
            print(f"连接成功 {self.player_list[len(self.player_list) - 1].login_username}")
        else:
            print("连接失败")

        # 如果他的名字和某一个一样 那就证明要不就重复登录 要不就重连
        x = 0
        for player in self.player_list:
            if self.player_list[len(self.player_list) - 1].login_username == player.login_username and x != len(self.player_list) - 1 and player.exist:
                self.disconnect(player.login_username)  # 因为先进来的排在前面，肯定会被先搜到，所以这样写没关系
                print(f"他的登录顶替了原来这个账号在player_list中的位置！")
                self.player_list.insert(x, self.player_list[-1])
                del self.player_list[x + 1]
                del self.player_list[-1]
            x += 1

    def disconnect(self, player_name):
        self.player_list[self.__from_name_find_place(player_name)].logout()
        self.player_list[self.__from_name_find_place(player_name)].online = False
        # if found someone disconnected numbered x
        # del player_online[0]

    def __from_name_find_place(self, name):
        x = 0
        for player in self.player_list:
            if player.login_username == name:
                return x
            x += 1
        return -1


print("PLAYER.PY IMPORTED")
