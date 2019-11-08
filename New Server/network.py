import socket, json, threading, time


def printb(string):
    global server
    print(f'\n【发给所有人】\n{string}')
    server.broadcast(message=string)
    time.sleep(0.16)


def printp(string, player):
    global server
    global player_ID
    print(f'\n【发给 {player_ID[player]} (玩家{player})】\n{string}')
    server.connections[player].send(json.dumps({
        'sender_id': -1,
        'sender_nickname': '',
        'message': string
    }).encode())
    time.sleep(0.08)
    # server.connections[player].send(bytes(string, 'UTF-8'))


def inputp(string, player):
    global waiting
    # waiting[0] 是玩家，[1]是内容
    printp(string, player)
    waiting = (None, None)
    while waiting[0] != player:
        time.sleep(0.33)
    if waiting[1] is not None:
        return int(waiting[1])
    return 0
    # 假如 就返回0


class Server:
    """
    服务器类
    """
    def __init__(self):
        """
        构造
        """
        global waiting
        global player_number
        player_number = 0
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = list()
        self.nicknames = list()

    def __user_thread(self, user_id):
        """
        用户子线程
        :param user_id: 用户id
        """
        global player_number
        global waiting
        global shoupai
        global gold
        global player_ID
        global owned_cards

        connection = self.connections[user_id]
        nickname = self.nicknames[user_id]
        print(f'玩家{user_id}(USER_ID) {nickname}(ID) {connection.fileno()}(fileno) 加入房间')
        player_number += 1
        try:
            self.broadcast(message=f'玩家 {nickname} ({user_id}) 已准备')
        except AttributeError:
            pass
        print(f"当前连接数{player_number}")
        '''
        print("检测人数")
        if player_number == 2:
            # self.broadcast(message=f'已有{player_number}人。正在等待服务器确认开始')
            printb(f'已有{player_number}人。正在等待服务器确认开始')
            printb('开始游戏')
            '''

        '''
            thread2 = threading.Thread(target=main())
            thread2.setDaemon(True)
            # 我把游戏线程也视为子线程
            thread2.start()
        '''

        # 侦听
        while True:
            # noinspection PyBroadException
            try:
                '''
                buffer = connection.recv(1024).decode()
                # 解析成json数据
                obj = json.loads(buffer)
                '''
                '''
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
                '''
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
                    try:
                        if obj['message'] == '手牌' or obj['message'] == 'shoupai':
                            # printp(f"\n你的手牌：{translate_shoupai(obj['sender_id'])}\n所有人的手牌数：{shoupai_count()}\n", obj['sender_id'])
                            full_string = f"\n你的手牌：{translate_shoupai(obj['sender_id'])}\n\n"
                            name = 0
                            while name < len(player_ID):
                                full_string += f'{player_ID[name]} (玩家 {name})：{shoupai_count()[name]}张牌\n'
                                name += 1
                            printp(full_string, obj['sender_id'])
                        elif obj['message'] == '金币' or obj['message'] == 'jinbi':
                            # printp(f"\n你的金币：{gold[obj['sender_id']]}\n所有人的金币：{gold}\n", obj['sender_id'])
                            full_string = f"\n你的金币：{gold[obj['sender_id']]}\n"
                            name = 0
                            while name < len(player_ID):
                                full_string += f'{player_ID[name]} (玩家 {name})：{gold[name]}金\n'
                                name += 1
                            printp(full_string, obj['sender_id'])
                        elif obj['message'] == '装备' or obj['message'] == 'zhuangbei':
                            # printp(f"\n所有人的装备：{translate_owned_cards()}\n", obj['sender_id'])
                            full_string = '\n'
                            name = 0
                            while name < len(player_ID):
                                full_string += f'{player_ID[name]} (玩家 {name})：{translate_card(owned_cards[name])}\n'
                                name += 1
                            printp(full_string, obj['sender_id'])
                        else:
                            self.broadcast(obj['sender_id'], obj['message'])
                            print(f"【聊天】{player_ID[obj['sender_id']]} ({obj['sender_id']}) 说：{obj['message']}")
                    except NameError:
                        printp('无法使用代码：游戏还没开始！', obj['sender_id'])
                elif obj['type'] == 'input':
                    waiting = (obj['sender_id'], obj['message'])
                    print(f"收到 {player_ID[obj['sender_id']]} (玩家{obj['sender_id']}) ：{obj['message']}，类型：{obj['type']}")
                elif obj['type'] == 'cheat':
                    try:
                        if obj['message'] == 'showmethemoney':
                            gold[obj['sender_id']] += 10
                            printb(f"{player_ID[obj['sender_id']]} (玩家 {obj['sender_id']}) 使用了作弊代码，获得10金。"
                                   f"\n当前金钱：{gold[obj['sender_id']]}")
                        elif obj['message'] == 'gimmeaspatula':
                            owned_cards[obj['sender_id']].append(38)
                            printb(f"{player_ID[obj['sender_id']]} (玩家 {obj['sender_id']}) 使用了作弊代码，获得金铲铲。"
                                   f"\n当前装备：{translate_card(owned_cards[obj['sender_id']])}")
                    except NameError:
                        printp('无法使用代码：游戏还没开始！', obj['sender_id'])
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
                    player_number -= 1
                    print(f"当前连接数{player_number}")
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
        global player_ID
        global player_number
        global jirenchang
        global version
        global gengxinshuoming
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

        # 清空ID
        player_ID = []
        conti = False

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
                        printp(f'\n{gengxinshuoming}\n\n已在房间中的有 {len(self.connections)} 人', len(self.connections) - 1)
                        '''
                        for item in player_ID:
                            printp(f"{item}", len(self.connections) - 1)
                        '''
                        # 上面两行效率太低了。改成有几个人在好了
                        printp(f'\n\n*******************\n本房间：\n结束条件：{end_game_items} 件装备\n'
                               f'人数：{jirenchang}\n*******************\n\n', len(self.connections) - 1)

                        # 开辟一个新的线程
                        thread = threading.Thread(target=self.__user_thread, args=(len(self.connections) - 1,))
                        thread.setDaemon(True)
                        thread.start()
                    # 到时候要删掉的
                    print('检测人数')
                    if player_number == jirenchang:
                        # 记得回来 我删掉试试看
                        '''
                        while len(player_ID) <= 8:
                           player_ID.append('')
                           # 用于填充playerID使得他不要out of range
                        '''
                        printb(f'已有{player_number}人。正在等待服务器确认开始')
                        printb(f'开始游戏')
                        thread2 = threading.Thread(target=main())
                        thread2.setDaemon(True)
                        # 我把游戏线程也视为子线程
                        thread2.start()
                elif obj['version'] != version:
                    connection.send(json.dumps({
                        'version': version
                    }).encode())
                    print(f'{connection.fileno()} 的版本过低。他的版本：{obj["version"]}')
                else:
                    print('无法解析json数据包:', connection.getsockname(), connection.fileno())

                    '''
                    while len(player_ID) <= 8:
                        player_ID.append('')
                        print('while 执行一次')
                        # 用于填充playerID使得他不要out of range
                    '''

            except OSError:  # 记得调回去
                print('断开连接:', connection.fileno())  # 这一行会出现OSError
                print(f"当前连接数{player_number}")
            except json.decoder.JSONDecodeError:
                print('JSONDecodeError:', connection.fileno())
                time.sleep(0.5)
                connection.close()
