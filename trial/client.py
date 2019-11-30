# -*- coding: cp936 -*-
import socket
import threading
import json
import os
import time


def clear():
    os.system('cls')
# 只能在Windows下使用


temp = os.system('title 监狱威龙客户端（控制台版）')
temp = os.system('MODE con: COLS=50 LINES=30')


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
                    if buffer == '':
                        break
                    if buffer[-1] == '}':
                        break

                # 解决黏包问题
                find = 0
                # print(type(fuffer))
                # print(f"fuffer = {fuffer}")
                fuffer_split = []
                while find < len(fuffer) - 1:
                    if fuffer[find] == "}" and fuffer[find + 1] == "{":
                        fuffer_split.append(fuffer[0:find + 1])  # 注意：包括开头，不包括结尾！
                        fuffer = fuffer[find + 1:-1]
                        find = -1
                    find += 1
                if fuffer_split:
                    print(f"fuffer_split = {fuffer_split}\n")
                    for item in fuffer_split:
                        obj = json.loads(item)
                        print(f"被分割: {obj}")
                    # fuffer_split.clear()
                else:
                    obj = json.loads(fuffer)
                    print(f"未被分割: {obj}")
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
        if username == 'admin' and password == 'admin':
            print('上帝模式已开启')
            self.god = True
            temp = os.system('title 上帝')
        # .split(' ')[0]
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
        thread = threading.Thread(target=self.__send_message_thread, args=(message, ))
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


version = '1.15'
client = Client()
client.start()
