import socket
import threading
import json


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




'''
import json
import os
import random
import socket
import threading
import time

class Server:
    """
    服务器类
    """
    def __init__(self):
        """
        构造
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = list()
        self.nicknames = list()

    def __user_thread(self, user_id):
        """
        用户子线程
        :param user_id: 用户id
        """

        connection = self.connections[user_id]
        nickname = self.nicknames[user_id]
        print(f'玩家{user_id}(USER_ID) {nickname}(ID) {connection.fileno()}(fileno) 加入房间')
        player_number += 1
        try:
            self.broadcast(message=f'玩家 {nickname} ({user_id}) 已准备')
        except AttributeError:
            pass
        print(f"当前连接数{player_number}")
        """
        print("检测人数")
        if player_number == 2:
            # self.broadcast(message=f'已有{player_number}人。正在等待服务器确认开始')
            printb(f'已有{player_number}人。正在等待服务器确认开始')
            printb('开始游戏')
            """

        """
            thread2 = threading.Thread(target=main())
            thread2.setDaemon(True)
            # 我把游戏线程也视为子线程
            thread2.start()
        """

        # 侦听
        while True:
            # noinspection PyBroadException
            try:
                """
                buffer = connection.recv(1024).decode()
                # 解析成json数据
                obj = json.loads(buffer)
                """
                """
                fuffer = ''
                # noinspection PyBroadException
                while True:
                    buffer = self.__socket.recv(1024).decode()
                    fuffer += buffer
                    # print(f"fuffer = {fuffer}")
                    # print(buffer)
                    if buffer == '':
                        break
                    if buffer[-1] == '}':
                        break
                obj = json.loads(fuffer)
                """
                # 解决断包问题
                fuffer = ''
                while True:
                    buffer = connection.recv(1024).decode()
                    fuffer += buffer
                    # print(f"fuffer = {fuffer}")
                    # print(buffer)
                    if buffer == '':
                        break
                    if buffer[-1] == '}':
                        break
                obj = json.loads(fuffer)
                # 如果是广播指令
                if obj['type'] == 'broadcast':
                    print("nih")
                else:
                    print('[Server] 无法解析json数据包:', connection.fileno(), self.nicknames[user_id])
                    #  connection.getsockname(), connection.fileno(),
            except OSError:
                # print(f'\n\n{buffer}\n\n')
                print('连接失效:', connection.fileno(), self.nicknames[user_id])
                self.connections[user_id].close()
                # self.connections[user_id] = None
                # self.nicknames[user_id] = None 我要开发断线重连 所以这个必须删掉
                player_number -= 1
                print(f"当前连接数{player_number}")
                break
            except json.decoder.JSONDecodeError:
                if buffer == '':
                    print(f'{self.nicknames[user_id]}已断开连接')
                    self.connections[user_id].close()
                    self.connections[user_id] = None
                    self.nicknames[user_id] = None
                    return
                print('JSONDecodeError:', connection.fileno(), self.nicknames[user_id])
                time.sleep(0.1)

    def broadcast(self, user_id=-1, message=''):
        """
        广播
        :param user_id: 用户id(-1为系统)
        :param message: 广播内容
        """
        for i in range(0, len(self.connections)):
            if user_id != i and self.connections[i] is not None:
                self.connections[i].send(json.dumps({
                    'sender_id': user_id,
                    'sender_nickname': self.nicknames[user_id],
                    'message': message
                }).encode())

    def start(self):
        """
        启动服务器
        """
        # 绑定端口
        self.__socket.bind(('192.168.1.111', 5555))
        # 启用监听
        self.__socket.listen(5)
        print(f'服务器已开启。当前版本：{version}，{jirenchang}人场')

        # 清空连接
        self.connections.clear()
        self.nicknames.clear()
        self.connections = []
        self.nicknames = []

        # 开始侦听
        while True:
            connection, address = self.__socket.accept()
            print('收到一个新连接', connection.fileno())

            # 尝试接受数据
            # noinspection PyBroadException
            try:
                buffer = connection.recv(1024).decode()
                # 解析成json数据
                obj = json.loads(buffer)
                # 如果是连接指令，那么则返回一个新的用户编号，接收用户连接
                if obj['type'] == 'login' and obj['version'] == version:
                    c = 0
                    cl = False
                    # cl 是重连变量
                    for item in player_ID:
                        if obj['nickname'] == item:
                            cl = True
                            player_ID.append(obj['nickname'])
                            connection.send(json.dumps({
                                'id': c
                            }).encode())
                            connection.send(json.dumps({
                                'sender_id': -1,
                                'message': f'欢迎重连，你的id：{c}，名字：{player_ID[c]}'
                            }).encode())
                            # printp(f'欢迎重连，你的id：{c}，名字：{player_ID[c]}', c)
                            conti = True
                            # 开辟一个新的线程
                            thread = threading.Thread(target=self.__user_thread, args=(c,))
                            thread.setDaemon(True)
                            thread.start()
                            break
                        c += 1
                    if conti == True:
                        conti = False
                        continue
                    if cl is False:
                        self.connections.append(connection)
                        self.nicknames.append(obj['nickname'])
                        player_ID.append(obj['nickname'])
                        connection.send(json.dumps({
                            'id': len(self.connections) - 1
                        }).encode())
                        # 开辟一个新的线程
                        thread = threading.Thread(target=self.__user_thread, args=(len(self.connections) - 1,))
                        thread.setDaemon(True)
                        thread.start()
                else:
                    print('无法解析json数据包:', connection.getsockname(), connection.fileno())

            except OSError: # 记得调回去
                print('断开连接:', connection.fileno())  # 这一行会出现OSError
                print(f"当前连接数{player_number}")
            except json.decoder.JSONDecodeError:
                print('JSONDecodeError:', connection.fileno())
                time.sleep(0.5)
                connection.close()
                '''