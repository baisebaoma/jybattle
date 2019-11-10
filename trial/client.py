# -*- coding: cp936 -*-
import socket
import threading
import json
import os
import time


def clear():
    os.system('cls')
# ֻ����Windows��ʹ��


class Client:
    """
    �ͻ���
    """

    def __init__(self):
        """
        ����
        """
        super().__init__()
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__id = None
        self.__nickname = None

    def __receive_message_thread(self):
        """
        ������Ϣ�߳�
        """
        global mute
        while True:
            fuffer = ''
            # noinspection PyBroadException
            try:
                # ����ϰ�����
                while True:
                    buffer = self.__socket.recv(1024).decode()
                    fuffer += buffer
                    # print(f"fuffer = {fuffer}")
                    # print(buffer)
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
                        if obj['sender_id'] == -1:
                            # ��-1��ϵͳ
                            print(obj['message'])
                        elif mute is False:
                            if obj['message'] == '?' or obj['message'] == '��':
                                print(f"�����졿[{obj['sender_nickname']} ({obj['sender_id']})] ʾ������Ѳ�����Ӱ")
                            else:
                                print(f"�����졿[{obj['sender_nickname']} ({obj['sender_id']})]˵��{obj['message']}")
                else:
                    obj = json.loads(fuffer)
                    if obj['sender_id'] == -1:
                        # ��-1��ϵͳ
                        print(obj['message'])
                    elif mute is False:
                        if obj['message'] == '?' or obj['message'] == '��':
                            print(f"�����졿[{obj['sender_nickname']} ({obj['sender_id']})] ʾ������Ѳ�����Ӱ")
                        else:
                            print(f"�����졿[{obj['sender_nickname']} ({obj['sender_id']})]˵��{obj['message']}")
                # �����ظ��˴��롣�ǵøġ�

                '''
                # print(f"obj = {obj}")
                # obj = json.loads(fuffer)
                if obj['sender_id'] == -1:
                    # ��-1��ϵͳ
                    print(obj['message'])
                elif mute is False:
                    if obj['message'] == '?' or obj['message'] == '��':
                        print(f"�����졿[{obj['sender_nickname']} ({obj['sender_id']})] ʾ������Ѳ�����Ӱ")
                    else:
                        print(f"�����졿[{obj['sender_nickname']} ({obj['sender_id']})]˵��{obj['message']}")
                # print(buffer)
                '''

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

    def __send_message_thread(self, message):
        """
        ������Ϣ�߳�
        :param message: ��Ϣ����
        """
        self.__socket.send(json.dumps({
            'type': 'broadcast',
            'sender_id': self.__id,
            'message': message
        }).encode())
        # ��ʾ�Լ����͵���Ϣ
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
        password = input("���룺")
        # .split(' ')[0]
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
            buffer = self.__socket.recv(1024).decode()
            obj = json.loads(buffer)
            clear()
            print(f'�ɹ���¼���յ������ݣ���{obj}��')
            # �������߳����ڽ�������
            thread = threading.Thread(target=self.__receive_message_thread)
            thread.setDaemon(True)
            thread.start()
        except json.decoder.JSONDecodeError:
            print('�޷��ӷ�������ȡ����')
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
        thread = threading.Thread(target=self.__send_message_thread, args=(message, ))
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


version = '1.15'
mute = False
client = Client()
client.start()
