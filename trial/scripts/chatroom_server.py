import json
import socket
import threading


class ChatServer:
    """
    服务器类
    """
    def __init__(self):
        """
        构造
        """
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __user_thread(self, user_id):
        """
        用户子线程
        :param user_id: 用户id
        """
        connection = None

        # 侦听
        while True:
            # noinspection PyBroadException
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

    def start(self):
        """
        启动服务器
        """
        # 绑定端口
        self.__socket.bind(('127.0.0.1', 8888))

        # 启用监听
        self.__socket.listen(5)
        print('服务器已启动')

        # 开始侦听
        while True:
            connection, address = self.__socket.accept()
            print('[Server] 收到一个新连接', connection.getsockname(), connection.fileno())

            # 尝试接受数据
            # noinspection PyBroadException
            # try:
            buffer = connection.recv(1024).decode()
            # 解析成json数据
            obj = json.loads(buffer)
            # 如果是连接指令，那么则返回一个新的用户编号，接收用户连接
            if obj['type'] == 'login':
                if obj["username"] == "admin" and obj["password"] == "admin":
                    print("爹来了")
                    # 给最高管理权限
                    p.admin.connection = connection
                    p.admin.connection.send(json.dumps({
                        'message': "连接成功"
                    }).encode())
                    thread = threading.Thread(target=p.admin.listen())
                    thread.setDaemon(True)
                    thread.start()

                elif p.connect(login_username=obj["username"], login_password=obj["password"]) == 0:
                    p.player_list[p.find(obj["username"])].connection = connection
                    p.player_list[p.find(obj["username"])].connection.send(json.dumps({
                        'sender_id': 0,
                        'message': "连接成功"
                    }).encode())
                else:
                    connection.send(json.dumps({
                        'sender_id': 0,
                        'message': "用户名或密码错误"
                    }).encode())
            elif obj['type'] == 'signup':



                '''
                self.__connections.append(connection)
                self.__nicknames.append(obj['username'])
                connection.send(json.dumps({
                    'id': len(self.__connections) - 1
                }).encode())
                '''
                # 开辟一个新的线程
                # thread = threading.Thread(target=self.__user_thread, args=(len(self.__connections) - 1, ))
                # thread.setDaemon(True)
                # thread.start()
            else:
                print('[Server] 无法解析json数据包:', connection.getsockname(), connection.fileno())
            # except Exception:
            #     print('[Server] 无法接受数据:', connection.getsockname(), connection.fileno())
            #     print(obj)