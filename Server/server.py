import socket
import json
import threading


def 接收消息(连接):
    # 输入连接，输出一个含有所有obj的list
    while True:
        全缓存 = ''
        obj分割 = list()
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
                    obj分割.append(json.loads(item))
                全缓存分割.clear()
                return obj分割
                # 玩家.处理信息(obj)
            else:
                obj = json.loads(全缓存)
                return list(obj)
        except OSError:
            print(f"{连接.getpeername()} 的连接已断开。")
            return
        # except OSError:
        except json.decoder.JSONDecodeError:
            if 全缓存 == '':
                print('\n可能是客户端关闭或BUG，无法接收信息。')
                return
            else:
                print(f'\n{全缓存}\n')
                print('可能是黏包问题，解码失败，无法显示这句话。')
                return


def 用户线程(连接):
    while True:
        消息列表 = 接收消息(连接)
        if 消息列表:
            for 消息 in 消息列表:
                处理消息(消息, 连接)
        else:
            return


def 处理消息(消息, 连接):
    print(f"来自 {连接.getpeername()} 的消息：{消息}")
    if 消息['类型'] == '登录':
        玩家控制.广播(类型='广播', 消息=f"{消息['用户名']} 已连接")
        玩家控制.玩家列表.append(玩家(用户名=消息['用户名'], 连接=连接))

    elif 消息['类型'] == '游戏':
        玩家控制.广播(类型='广播', 消息=f"你获得了 {消息['消息']}！")


class 玩家:
    def __init__(self, 用户名='', 连接=None):
        self.用户名 = 用户名
        self.连接 = 连接
        self.房间 = 0  # 0是大厅
    pass


class 玩家控制:
    玩家列表 = list()

    @classmethod
    def 广播(cls, **字典):
        print(f"广播：{字典['消息']}")
        for 对象 in cls.玩家列表:
            对象.连接.send(json.dumps(字典).encode())


套接字 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
套接字.bind(('127.0.0.1', 8888))
套接字.listen(5)
while True:
    连接, 地址 = 套接字.accept()
    print('收到一个新连接', 连接.getpeername(), 连接.fileno())
    # 第一步检查版本号
    线程 = threading.Thread(target=用户线程, args=(连接,), daemon=True)
    线程.start()


