import os
import socket
import json
import time
import threading
import client.game
import client.UI
import webbrowser


class 网络:
    """
    客户端
    """
    套接字 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    发送锁 = True  # True 代表可发，False 代表不可发
    用户名 = ""

    @classmethod
    def 接收消息(cls):
        """
        返回一个列表，里面包含这次接收的消息
        """
        全缓存 = ''
        事件分割 = list()
        try:
            # 解决断包问题
            while True:
                缓存 = cls.套接字.recv(1024).decode()
                全缓存 += 缓存
                if 缓存 == '' or 缓存[-1] == '}':
                    break

            # 解决黏包问题
            指针 = 0
            全缓存分割 = []
            while 指针 < len(全缓存) - 1:
                if 全缓存[指针] == "}" and 全缓存[指针 + 1] == "{":
                    全缓存分割.append(全缓存[0:指针 + 1])  # 注意：包括开头，不包括结尾！
                    全缓存 = 全缓存[指针 + 1:]
                    指针 = -1
                指针 += 1
            全缓存分割.append(全缓存)
            if 全缓存分割:
                for 对象 in 全缓存分割:
                    事件分割.append(json.loads(对象))
                return 事件分割
            else:
                事件 = json.loads(全缓存)
                return list(事件)
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
        finally:
            return 事件分割

    @classmethod
    def __receive_message_thread(cls):
        """
        接受消息线程
        """
        while True:
            全缓存 = ''
            事件分割 = list()
            try:
                # 解决断包问题
                while True:
                    缓存 = cls.套接字.recv(1024).decode()
                    全缓存 += 缓存
                    if 缓存 == '' or 缓存[-1] == '}':
                        break

                # 解决黏包问题
                指针 = 0
                全缓存分割 = []
                while 指针 < len(全缓存) - 1:
                    if 全缓存[指针] == "}" and 全缓存[指针 + 1] == "{":
                        全缓存分割.append(全缓存[0:指针 + 1])  # 注意：包括开头，不包括结尾！
                        全缓存 = 全缓存[指针 + 1:]
                        指针 = -1
                    指针 += 1
                全缓存分割.append(全缓存)
                if 全缓存分割:
                    for 对象 in 全缓存分割:
                        事件分割.append(json.loads(对象))
                    cls.处理(事件分割)
                else:
                    事件 = json.loads(全缓存)
                    cls.处理(list(事件))
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
    def 发送(cls, **字典):
        if cls.发送锁:
            字典['用户'] = cls.用户名
            cls.套接字.send(json.dumps(字典).encode())

    @classmethod
    def 处理(cls, 事件列表):
        # client.game.游戏.消息队列.append(f"{事件列表}")  # 调试用
        for 对象 in 事件列表:
            cls.消息翻译(对象)

    @classmethod
    def 消息翻译(cls, 对象):

        # 下面这个不应该存在，因为服务器不应该直接发送文本给客户端显示
        """
        if 对象['类型'] == '广播':
            # print(对象['消息'])
            # client.game.游戏.消息队列.append(对象['消息'])
            client.UI.UI.refresh()
        """

        # 下面这个不应该存在，因为服务器不应该直接发送控制给客户端显示
        """
        elif 对象['类型'] == '控制':
            # if 对象['列表'] == ['clear']:
            #     client.game.游戏.控制.clear()
            if 对象['列表'] == ['disable']:
                cls.发送锁 = False
            elif 对象['列表'] == ['enable']:
                cls.发送锁 = True
            else:
                client.game.游戏.控制.clear()
                for 控制 in 对象['列表']:
                    client.game.游戏.控制.append(控制)
                client.UI.UI.refresh()
        """
        if 对象['用户'] != '系统':
            pass
            if 对象['行为'] == '登录':
                # client.game.游戏.消息队列.append(f"{对象['用户名']} 已登录")
                if 对象['用户'] == cls.用户名:
                    client.game.游戏.消息队列.append(f"{对象['用户']} （你自己） 已登录")
                    client.game.游戏.控制.append("准备")
                    client.game.游戏.自己 = client.game.玩家(对象['用户'])
                    client.game.游戏.自己.积分 += 10
                else:
                    client.game.游戏.消息队列.append(f"{对象['用户']} 已登录")
                    client.game.游戏.玩家列表.append(client.game.玩家(对象['用户']))

            elif 对象['行为'] == '准备':
                if 对象['用户'] == cls.用户名:
                    client.game.游戏.消息队列.append(f"{对象['用户']} （你自己） 已准备")
                    client.game.游戏.控制 = ["已准备"]
                    cls.发送锁 = False
                else:
                    client.game.游戏.玩家列表.搜索(对象['用户']).准备 = True
                    client.game.游戏.消息队列.append(f"{对象['用户']} 已准备")

        else:
            if 对象['行为'] == '游戏开始':
                client.game.游戏.消息队列.append(f"游戏开始了！")

    @classmethod
    def 登录(cls):
        # 将用户名发送给服务器
        while True:
            cls.用户名 = input('用户名: ')
            print('正在尝试登录。\n')
            cls.套接字.send(json.dumps({
                '用户': cls.用户名,
                '行为': '登录',
                '对象': 2.2
            }).encode())
            # cls.套接字.recv(1024).decode()
            消息 = cls.接收消息()

            if 消息[0]['行为'] == '拒绝登录：重名':
                print('选择了一个和已存在玩家重复的名字。请重试。')

            elif 消息[0]['行为'] == '拒绝登录：版本':
                print(f"你的版本过低。请至：{消息[0]['对象']} 更新版本。")
                webbrowser.open(消息[0]['对象'])

            elif 消息[0]['行为'] == '成功登录':
                print(f"登录成功")
                cls.处理(消息[1:])
                break
            time.sleep(1)

            cls.处理(消息[1:])

        try:
            # 开启子线程用于接受数据
            thread = threading.Thread(target=cls.__receive_message_thread)
            thread.setDaemon(True)
            # 如果Daemon，那么webbrowser.open那句话就没用了
            # 现在好像又有用了？搞不清
            thread.start()
        except json.decoder.JSONDecodeError:
            print(f'解码错误')

    @classmethod
    def start(cls):
        """
        启动客户端
        """
        try:
            cls.套接字.connect(('127.0.0.1', 8888))
            cls.登录()
        except ConnectionRefusedError:
            print('本地服务器未开启！请联系开发者。')

