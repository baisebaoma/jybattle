# -*- coding: cp936 -*-
import operator
import socket
import threading
import json
import os
import time
import random

��� = 64
�߶� = 65

os.system('title ���������ͻ��ˣ�����̨�棩')
os.system(f'MODE con: COLS={���} LINES={�߶�}')


class UI:
    """UI�ฺ�����еģ����ְ汾�ģ�UI����"""
    ��ֱͬ�� = True
    if ��ֱͬ��:
        ����� = ''

    @classmethod
    def printc(cls, ����):  # ȫ�ֿ��ƾ��������ֻҪ��ֱͬ����True �ͻᱣ�浽�������
        global ���
        ���ּ��� = 0
        �ܹ����� = 0
        ��� = ''
        for �� in ����:
            if '\u4e00' <= �� <= '\u9fa5':
                ���ּ��� += 1
            �ܹ����� += 1
        �ո��� = ��� // 2 - �ܹ����� // 2 - ���ּ��� // 2
        if �ո��� < 0:
            �ո��� = 0
        ��� = ' ' * �ո��� + ����
        if cls.��ֱͬ��:
            if ���� == '\n':
                cls.����� += '\n'
            else:
                cls.����� += ��� + '\n'
        else:
            if ���� == '\n':
                print()
            else:
                print(���)

    @staticmethod
    def ����Ӣ�۳�(�б�):  # ��ӡ�б�
        if not �б�:
            return '��'
        �ַ��� = ''
        for Ӣ�� in �б�:
            �ַ��� += f'{Ӣ��} '
        return �ַ���

    '''
    @classmethod
    def __print(cls, ����):  # ��дprint���ﵽ���ƴ�ֱͬ����Ŀ��
        if cls.��ֱͬ��:
            cls.����� += ���� + '\n'
        else:
            print(����)
    '''

    @staticmethod
    def cls():
        os.system('cls')

    @classmethod
    def draw_line(cls, number=None, ID = None):
        if number and ID:
            cls.printc(f"-- {number} {ID} --")
        else:
            cls.printc("  ---------------------------------------------------  ")

    @classmethod
    def draw_rank(cls, ��Ϸ):
        rank = 1
        cls.draw_line()
        # cls.printc("���а�")
        # cls.draw_line()
        # cls.draw_line()
        for ��� in ��Ϸ.����б�:
            cls.draw_line(number=rank, ID=���.ID)
            cls.printc(f"��{���.��ɫ}��")
            # print(' ' * 10 + str(���.��ɫ))
            cls.printc(f"{���.���}���" + ' ' * 3 + \
                       f"{���.����}����" + ' ' * 3 + str(���.����) + '����')
            cls.printc(cls.����Ӣ�۳�(���.Ӣ�۳�))
            if rank != len(��Ϸ.����б�):
                cls.printc('\n')
            rank += 1

    @classmethod
    def draw_message(cls, ��Ϸ):
        cls.draw_line()
        # cls.printc("ͨ����")
        # cls.draw_line()
        ���� = 10
        while len(��Ϸ.��Ϣ����) > ����:
            del ��Ϸ.��Ϣ����[0]
        for ��Ϣ in ��Ϸ.��Ϣ����:
            cls.printc(��Ϣ)
        if len(��Ϸ.��Ϣ����) < ����:
            for i in range(1, ���� + 1 - len(��Ϸ.��Ϣ����)):
                cls.printc('\n')

    @classmethod
    def draw_card(cls, ��Ϸ):
        pass

    @classmethod
    def draw_round(cls, ��Ϸ):
        cls.printc(f"��{��Ϸ.�غ�}�غ�")

    @classmethod
    def draw_control(cls, ��Ϸ):
        cls.draw_line()
        # cls.printc("������")
        # cls.draw_line()
        cls.draw_card(��Ϸ.����)

    @classmethod
    def refresh(cls, ��Ϸ):
        cls.cls()
        cls.draw_round(��Ϸ)
        cls.draw_message(��Ϸ)
        cls.draw_rank(��Ϸ)
        cls.draw_control(��Ϸ)
        if cls.��ֱͬ��:
            print(cls.�����)
            cls.����� = ''


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
    class ����б���(list):
        def __init__(self, *args):
            super().__init__(*args)

        def ����(self, ID):
            for ��� in self:
                # print(���.ID)
                if ���.ID == ID:
                    return ���
    ������ = '' + '�ķ���'
    ����б� = ����б���()
    ��Ϣ���� = list()
    ���� = None
    ���� = None
    ���� = list()
    �غ� = 1


'''
    def ��ֵ(self, ���, ��Ϣ, �޸���):  # �϶�����ID���Ѱ� ����ɵ��
        self.����б�[a.����б�.index(pzk)].��� += 2
        '''

a = ��Ϸ()

a.��Ϣ���� = ["�����ֵ�ѡ�� �������ƶ�ʦ ������ж���", "ѡ�� �������ƶ�ʦ ������� pzk ��", "pzk ����ѡ�������ƻ��߽��"]

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


a.���� = "�����ڿ���ʹ��һ������"
'''
print("\033[31m���Ǻ�ɫ����\033[0m")
print("\033[32m������ɫ����\033[0m")
print("\033[33m���ǻ�ɫ����\033[0m")
print("\033[34m������ɫ����\033[0m")
print("\033[38m����Ĭ������\033[0m")
print("\033[7m����Ĭ�Ϻ�ɫ���屳����ɫ\033[0m")
'''

while True:
    index = random.randint(1, 3)
    if index == 1:
        a.��Ϣ����.append("pzk �ѻ��2��")
        a.����б�.����('pzk').��� += 2
    elif index == 2:
        a.��Ϣ����.append("pzk ����ʹ�ü���")
    elif index == 3:
        a.����б�.����('pzk').��� -= 13
        a.��Ϣ����.append("pzk ���� 13 �𣬲���� xjb �� ����˹��")
    UI.refresh(��Ϸ=a)
    time.sleep(0.5)

version = '1.15'

time.sleep(100)

# client = Client()
# client.start()
