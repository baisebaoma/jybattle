# -*- coding: cp936 -*-
import operator
import socket
import threading
import json
import os
import time

os.system('title ���������ͻ��ˣ�����̨�棩')
os.system('MODE con: COLS=55 LINES=50')


class UI:
    """UI�ฺ�����еģ����ְ汾�ģ�UI����"""

    @staticmethod
    def cls():
        os.system('cls')

    @classmethod
    def draw_player(cls, ��Ϸ):
        rank = 1
        print("  ���а�")
        print("  ---------------------------------------------------")
        for ��� in ��Ϸ.����б�:
            print(' ' * 2 + str(rank) + "��" + str(���.ID) + ' ' * 1 + str(���.��ɫ))
            # print(' ' * 10 + str(���.��ɫ))
            print(' ' * 9 + f"\033[33m{str(���.���)}���\033[0m" + ' ' * 3 \
                  + f"\033[34m{str(���.����)}����\033[0m" + ' ' * 3 + str(���.����) + '����')
            print(' ' * 11 + f"{str(���.Ӣ�۳�)}")
            print("  ---------------------------------------------------")
            rank += 1

    @classmethod
    def draw_message(cls):
        print("     �����ֵ�ѡ�� �������ƶ�ʦ ������ж���")

    @classmethod
    def draw_ui(cls, ��Ϸ):
        cls.draw_player(��Ϸ)
        cls.draw_message()


class ���:
    def __init__(self, ID):
        self.ID = ID
        self.��� = 0
        self.��ɫ = None  # None = δ����
        self.Ӣ�۳� = list()
        self.���� = None  # ���ڱ����ң�ֻ�ܿ������������ǲ��ܿ���������
        self.���� = 0


class Client:
    """
    �ͻ���
    """

    def __init__(self):
        """
        ����
        """
        super().__init__()
        self.god = False
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__id = None
        self.__nickname = None

    def __receive_message_thread(self):
        """
        ������Ϣ�߳�
        """
        while True:
            # noinspection PyBroadException
            try:
                fuffer = ''

                # ����ϰ�����
                while True:
                    # time.sleep(0.1)
                    buffer = self.__socket.recv(1024).decode()
                    fuffer += buffer
                    if buffer == '' or buffer[-1] == '}':
                        break

                # ���������
                find = 0
                # print(type(fuffer))
                # print(f"fuffer = {fuffer}")
                fuffer_split = []
                while find < len(fuffer) - 1:
                    if fuffer[find] == "}" and fuffer[find + 1] == "{":
                        fuffer_split.append(fuffer[0:find + 1])  # ע�⣺������ͷ����������β��
                        fuffer = fuffer[find + 1:]
                        find = -1
                    find += 1
                # print(f"current fuffer = {fuffer}")
                fuffer_split.append(fuffer)
                if fuffer_split:
                    # print(f"fuffer_split = {fuffer_split}\n")
                    for item in fuffer_split:
                        obj = json.loads(item)
                        print(f"{obj}")
                    # fuffer_split.clear()
                else:
                    obj = json.loads(fuffer)
                    print(f"{obj}")
                # �����ظ��˴��롣�ǵøġ�
            except OSError:
                print('�޷��ӷ�������ȡ����')
                return
            # except OSError:
            except json.decoder.JSONDecodeError:
                # print(f"\n\n\nfuffer\n\n\n")
                # print(f'obj = {obj}')
                if fuffer == '':
                    print('\n�����Ƿ������رջ�BUG���޷�������Ϣ��')
                    time.sleep(30)
                else:
                    print(f'\n{fuffer}\n')
                    print('�����������⣬����ʧ�ܣ��޷���ʾ��仰��')

            """
            ԭʼ
                    while True:
            fuffer = ''
            # noinspection PyBroadException
            try:
                # ����ϰ�����
                while True:
                    buffer = self.__socket.recv(1024).decode()
                    fuffer += buffer
                    if buffer == '':
                        break
                    if buffer[-1] == '}':
                        break

                # ���������
                find = 0
                fuffer_split = []
                while find < len(fuffer) - 1:
                    if fuffer[find] == "}" and fuffer[find + 1] == '{':
                        fuffer_split.append(fuffer[0:find + 1])  # ע�⣺������ͷ����������β��
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
                # �����ظ��˴��롣�ǵøġ�

            except OSError:
                print('�޷��ӷ�������ȡ����')
                return
            # except OSError:
            except json.decoder.JSONDecodeError:
                # print(f"\n\n\nfuffer\n\n\n")
                # print(f'obj = {obj}')
                if fuffer == '':
                    print('\n�����Ƿ������رջ�BUG���޷�������Ϣ��')
                    time.sleep(30)
                else:
                    print(f'\n{fuffer}\n')
                    print('�����������⣬����ʧ�ܣ��޷���ʾ��仰��')
            """

            """
            # û�н��ճ���ϰ�����İ汾
            try:
                buffer = self.__socket.recv(1024).decode()
                obj = json.loads(buffer)
                print(obj)
                # �����ظ��˴��롣�ǵøġ�
            except OSError:
                print('�޷��ӷ�������ȡ����')
                return
                # except OSError:
            except json.decoder.JSONDecodeError:
                print(f"����ʧ��, buffer = {buffer}, obj = {obj}")
            # print(f"\n\n\nfuffer\n\n\n")
            # print(f'obj = {obj}')
            """

    def __send_message_thread(self, type, message):
        """
        ������Ϣ�߳�
        :param message: ��Ϣ����
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
                print("ȱ������")
        else:
            self.__socket.send(json.dumps({
                'type': type,
                'message': message
            }).encode())
        '''
print(f"""��Ǹ����İ汾���ͣ��������ѶϿ���������ӡ�
�������汾��{obj['version']}����İ汾��{version}��
����ϵ�����߻�����°汾��""")'''

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
        ��¼������
        :param args: ����
        """
        global version
        username = input("�û�����")
        # password = input("���룺")
        password = 1
        # ���ǳƷ��͸�����������ȡ�û�id
        self.__socket.send(json.dumps({
            'type': 'login',
            'username': username,
            'password': password,
            'version': version,
        }).encode())
        # ���Խ�������
        # noinspection PyBroadException
        try:
            # buffer = self.__socket.recv(1024).decode()
            # obj = json.loads(buffer)
            # clear()
            # print(f'��¼�����ѷ��ͣ���{obj}��')
            # �������߳����ڽ�������
            thread = threading.Thread(target=self.__receive_message_thread)
            thread.setDaemon(True)
            thread.start()
        except json.decoder.JSONDecodeError:
            print('�������{obj}')
        except KeyError:
            clear()
            print(f'����°汾��\n��ǰ�ͻ��˰汾��{version}\n�������汾��{obj["version"]}')
            exit()

    def do_send(self, args):
        """
        ������Ϣ
        :param args: ����
        """
        message = args
        # �������߳����ڷ�������
        thread = threading.Thread(target=self.__send_message_thread, args=(message,))
        thread.setDaemon(True)
        thread.start()

    def start(self):
        global version
        """
        �����ͻ���
        """
        try:
            print(f'�������� �ͻ���\n\n�汾��{version}��\n\n')
            self.__socket.connect(('127.0.0.1', 8888))
            # self.__socket.connect(('47.98.179.115', 34674))
            print('���ڳ��Ե�¼��\n')
            self.do_login()
        except ConnectionRefusedError:
            print('���ط�����δ����������ϵ�����ߡ�')
        while True:
            self.do_send(input())


class ��Ϸ:
    ����б� = list()


a = ��Ϸ()

xjb = ���('xjb')
xjb.��� = 10
xjb.��ɫ = '����������������Ȼ����������������ϵ�'
xjb.Ӣ�۳� = ['����˹', '����', '����']
xjb.���� = 1
xjb.���� = 20

zer = ���('zer')
zer.��� = 7
zer.��ɫ = 'Ǳ��'
zer.Ӣ�۳� = ['��ɯ', '��', 'è']
zer.���� = 7
zer.���� = 14

zxx = ���('zxx')
zxx.��� = 0
zxx.��ɫ = '���ǿ���֮��'
zxx.Ӣ�۳� = ['��ϣ', '����', '����']
zxx.���� = 7
zxx.���� = 36

pzk = ���('pzk')
pzk.��� = 2
pzk.��ɫ = '�������ƶ�ʦ'
pzk.Ӣ�۳� = ['������', '����', '����']
pzk.���� = 0
pzk.���� = 26

tym = ���('tym')
tym.��� = 37
tym.��ɫ = 'Ǳ��'
tym.Ӣ�۳� = []
tym.���� = 6
tym.���� = 0

sxd = ���('sxd')
sxd.��� = 9
sxd.��ɫ = 'Ǳ��'
sxd.Ӣ�۳� = ['������', '����']
sxd.���� = 2
sxd.���� = 8

zhl = ���('zhl')
zhl.��� = 2
zhl.��ɫ = 'KoKou'
zhl.Ӣ�۳� = ['ϼ', '̩̹', '������']
zhl.���� = 0
zhl.���� = 18

cbt = ���('cbt')
cbt.��� = 8
cbt.��ɫ = 'Ǳ��'
cbt.Ӣ�۳� = ['����', '��Ѫ��', '��ʯ']
cbt.���� = 0
cbt.���� = 26

a.����б�.append(zer)
a.����б�.append(xjb)
a.����б�.append(zxx)
a.����б�.append(pzk)
a.����б�.append(tym)
a.����б�.append(sxd)
a.����б�.append(zhl)
a.����б�.append(cbt)

cmpfun = operator.attrgetter('����')
a.����б�.sort(key=cmpfun, reverse=True)

'''
print("\033[31m���Ǻ�ɫ����\033[0m")
print("\033[32m������ɫ����\033[0m")
print("\033[33m���ǻ�ɫ����\033[0m")
print("\033[34m������ɫ����\033[0m")
print("\033[38m����Ĭ������\033[0m")
print("\033[7m����Ĭ�Ϻ�ɫ���屳����ɫ\033[0m")
'''

while True:
    UI.draw_ui(��Ϸ=��Ϸ)
    time.sleep(1)
    UI.cls()

version = '1.15'

time.sleep(100)

# client = Client()
# client.start()
