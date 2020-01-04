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
            全缓存分割 = list()
            while 指针 < len(全缓存) - 1:
                if 全缓存[指针] == "}" and 全缓存[指针 + 1] == "{":
                    全缓存分割.append(全缓存[0:指针 + 1])  # 注意：包括开头，不包括结尾！
                    全缓存 = 全缓存[指针 + 1:]
                    指针 = -1
                指针 += 1
            全缓存分割.append(全缓存)
            if 全缓存分割:
                for item in 全缓存分割:
                    obj分割.append(json.loads(item))
                全缓存分割.clear()
                return obj分割
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
        for 对象 in 玩家控制.玩家列表:
            if 对象.用户名 == 消息['用户名']:
                print("尝试登录的用户选择了一个和已存在用户相同的用户名。请重试。")
                return

        玩家控制.玩家列表.append(玩家(用户名=消息['用户名'], 连接=连接))

        # 给这个登录的人发送当前的玩家列表
        for 对象 in 玩家控制.玩家列表:
            玩家控制.私发(消息['用户名'], 类型='登录', 用户名=f"{对象.用户名}")

        # 给这个登录的人发送玩家是否准备
        for 对象 in 玩家控制.玩家列表:
            if 对象.准备 is True:
                玩家控制.广播(类型='广播', 消息=f"{对象.用户名} 已准备！")

        # 给这个登录的人发送控制消息（准备）
        玩家控制.控制(消息['用户名'], 列表=["准备"])

        # 给其他的人发送这个人连接的消息
        for 对象 in 玩家控制.玩家列表:
            if 对象.用户名 != 消息['用户名']:
                对象.发送(类型='登录', 用户名=f"{消息['用户名']}")

    elif 消息['类型'] == '游戏':
        if 消息['消息'] == '准备':
            玩家控制.搜索(消息['用户名']).准备 = True
            print(f"{消息['用户名']} 已准备")
            玩家控制.广播(类型='广播', 消息=f"{消息['用户名']} 已准备！")
            玩家控制.控制(消息['用户名'], 列表=["disable"])
            玩家控制.控制(消息['用户名'], 列表=["已准备，正在等待所有玩家准备"])
            全玩家准备 = True
            for 对象 in 玩家控制.玩家列表:
                if 对象.准备 is False:
                    全玩家准备 = False
                    break
            if 全玩家准备 and len(玩家控制.玩家列表) >= 4:  # and 房主开始:
                玩家控制.广播(类型='广播', 消息=f"所有玩家已准备！游戏开始！")
                # 游戏开始
                线程 = threading.Thread(target=游戏.启动, args=(), daemon=True)
                线程.start()

        else:
            玩家控制.广播(类型='广播', 消息=f"{消息['用户名']} 选择了 {消息['消息']}！")


class 玩家:
    金币 = 0
    手牌 = list()
    装备 = list()

    房主 = False
    准备 = False

    def __init__(self, 用户名='', 连接=None):
        self.用户名 = 用户名
        self.连接 = 连接

    def 发送(self, **字典):
        print(f"私发给 {self.用户名} ：{字典}")
        self.连接.send(json.dumps(字典).encode())

    def 控制(self, **字典):
        print(f"私发控制给 {self.用户名} ：{字典}")
        字典['类型'] = '控制'
        self.连接.send(json.dumps(字典).encode())


class 玩家控制:
    玩家列表 = list()

    @classmethod
    def 广播(cls, **字典):
        print(f"广播：{字典}")
        for 对象 in cls.玩家列表:
            对象.连接.send(json.dumps(字典).encode())

    @classmethod
    def 私发(cls, ID, **字典):
        print(f"私发给 {ID} ：{字典}")
        cls.搜索(ID).连接.send(json.dumps(字典).encode())

    @classmethod
    def 控制(cls, ID, **字典):
        print(f"私发控制给 {ID} ：{字典}")
        字典['类型'] = '控制'
        cls.搜索(ID).连接.send(json.dumps(字典).encode())

    @classmethod
    def 搜索(cls, ID):
        for 对象 in cls.玩家列表:
            if 对象.用户名 == ID:
                return 对象


class 游戏:
    牌堆 = list()
    弃牌堆 = list()
    英雄池 = list()

    @classmethod
    def 启动(cls):

        # 初始化
        for 对象 in 玩家控制.玩家列表:
            对象.金币 = 2

    @classmethod
    def 向客户端发送数据(cls):
        pass



套接字 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
套接字.bind(('127.0.0.1', 8888))
套接字.listen(5)
while True:
    连接, 地址 = 套接字.accept()
    print('收到一个新连接', 连接.getpeername(), 连接.fileno())
    # 第一步检查版本号
    线程 = threading.Thread(target=用户线程, args=(连接,), daemon=True)
    线程.start()


