import os
import socket
import json
import time
import threading


class 网络:
    """
    客户端
    """
    套接字 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    @classmethod
    def __receive_message_thread(cls):
        """
        接受消息线程
        """
        while True:
            # noinspection PyBroadException
            全缓存 = ''
            try:
                # 解决断包问题
                while True:
                    # time.sleep(0.1)
                    缓存 = cls.套接字.recv(1024).decode()
                    全缓存 += 缓存
                    if 缓存 == '' or 缓存[-1] == '}':
                        break

                # 解决黏包问题
                指针 = 0
                # print(type(fuffer))
                # print(f"fuffer = {fuffer}")
                全缓存分割 = []
                while 指针 < len(全缓存) - 1:
                    if 全缓存[指针] == "}" and 全缓存[指针 + 1] == "{":
                        全缓存分割.append(全缓存[0:指针 + 1])  # 注意：包括开头，不包括结尾！
                        全缓存 = 全缓存[指针 + 1:]
                        指针 = -1
                    指针 += 1
                # print(f"current fuffer = {fuffer}")
                全缓存分割.append(全缓存)
                if 全缓存分割:
                    # print(f"fuffer_split = {fuffer_split}\n")
                    for item in 全缓存分割:
                        事件 = json.loads(item)
                        cls.处理(事件)
                else:
                    事件 = json.loads(全缓存)
                    cls.处理(事件)
            except OSError:
                print('无法从服务器获取数据')
                return
            except json.decoder.JSONDecodeError:
                if not 全缓存:
                    print('\n可能是服务器关闭或BUG，无法接收信息。')
                    time.sleep(30)
                else:
                    print(f'\n{全缓存}\n')
                    print('可能是黏包问题，解码失败，无法显示这句话。')

    @classmethod
    def __send_message_thread(cls, 类型, 内容):
        """
        发送消息线程
        :param message: 消息内容
        """
        cls.套接字.send(json.dumps({
            'type': 类型,
            'message': 内容
        }).encode())

    @classmethod
    def 处理(cls, 事件):
        print(事件)

    def 登录(self):
        """
        登录聊天室
        :param args: 参数
        """
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
        try:
            # 开启子线程用于接受数据
            thread = threading.Thread(target=self.__receive_message_thread)
            thread.setDaemon(True)
            thread.start()
        except json.decoder.JSONDecodeError:
            print(f'解码错误，')
        except KeyError:
            # clear()
            print(f'请更新版本。')

    def start(self):
        """
        启动客户端
        """
        try:
            self.套接字.connect(('127.0.0.1', 8888))
            # self.__socket.connect(('47.98.179.115', 34674))
            print('正在尝试登录。\n')
            self.登录()
        except ConnectionRefusedError:
            print('本地服务器未开启！请联系开发者。')