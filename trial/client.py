# -*- coding: cp936 -*-
import socket
import threading
import json
import os
import time


def clear():
    os.system('cls')
# 只能在Windows下使用


class Client:
    """
    客户端
    """

    def __init__(self):
        """
        构造
        """
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__id = None
        self.__nickname = None

    def __receive_message_thread(self):
        """
        接受消息线程
        """
        global mute
        while True:
            fuffer = ''
            # noinspection PyBroadException
            try:
                # 解决断包问题
                while True:
                    buffer = self.__socket.recv(1024).decode()
                    fuffer += buffer
                    # print(f"fuffer = {fuffer}")
                    # print(buffer)
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
                        if obj['sender_id'] == -1:
                            # 让-1是系统
                            print(obj['message'])
                        elif mute is False:
                            if obj['message'] == '?' or obj['message'] == '？':
                                print(f"【聊天】[{obj['sender_nickname']} ({obj['sender_id']})] 示意敌人已不见踪影")
                            else:
                                print(f"【聊天】[{obj['sender_nickname']} ({obj['sender_id']})]说：{obj['message']}")
                else:
                    obj = json.loads(fuffer)
                    if obj['sender_id'] == -1:
                        # 让-1是系统
                        print(obj['message'])
                    elif mute is False:
                        if obj['message'] == '?' or obj['message'] == '？':
                            print(f"【聊天】[{obj['sender_nickname']} ({obj['sender_id']})] 示意敌人已不见踪影")
                        else:
                            print(f"【聊天】[{obj['sender_nickname']} ({obj['sender_id']})]说：{obj['message']}")
                # 这里重复了代码。记得改。

                '''
                # print(f"obj = {obj}")
                # obj = json.loads(fuffer)
                if obj['sender_id'] == -1:
                    # 让-1是系统
                    print(obj['message'])
                elif mute is False:
                    if obj['message'] == '?' or obj['message'] == '？':
                        print(f"【聊天】[{obj['sender_nickname']} ({obj['sender_id']})] 示意敌人已不见踪影")
                    else:
                        print(f"【聊天】[{obj['sender_nickname']} ({obj['sender_id']})]说：{obj['message']}")
                # print(buffer)
                '''

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

    def __send_message_thread(self, message):
        """
        发送消息线程
        :param message: 消息内容
        """
        self.__socket.send(json.dumps({
            'type': 'broadcast',
            'sender_id': self.__id,
            'message': message
        }).encode())
        # 显示自己发送的消息
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
        password = input("密码：")
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
            buffer = self.__socket.recv(1024).decode()
            obj = json.loads(buffer)
            clear()
            print(f'成功登录，收到的数据：【{obj}】')
            # 开启子线程用于接受数据
            thread = threading.Thread(target=self.__receive_message_thread)
            thread.setDaemon(True)
            thread.start()
        except json.decoder.JSONDecodeError:
            print('无法从服务器获取数据')
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
mute = False
client = Client()
client.start()
