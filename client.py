# -*- coding: cp936 -*-
import operator
import random
import client.kbdlistener
import threading
from client.game import *
from client.network import *
from client.UI import *

# ��Ķ����� import

UI.��ֱͬ�� = True
UI.��� = 60
UI.�߶� = 65
UI.����ı�()

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

a.���� = ["è", '����', 'è', '����˹', '����', '������']
'''
print("\033[31m���Ǻ�ɫ����\033[0m")
print("\033[32m������ɫ����\033[0m")
print("\033[33m���ǻ�ɫ����\033[0m")
print("\033[34m������ɫ����\033[0m")
print("\033[38m����Ĭ������\033[0m")
print("\033[7m����Ĭ�Ϻ�ɫ���屳����ɫ\033[0m")
'''


while True:
    action = random.randint(1, 3)
    player = a.����б�[random.randint(0, 7)]
    if action == 1:
        a.��Ϣ����.append(f"{player.ID} �ѻ��2��")
        a.����б�.����(player.ID).��� += 2
    elif action == 2:
        a.��Ϣ����.append(f"{player.ID} ����ʹ�ü���")
    elif action == 3:
        if a.����б�.����(player.ID).��� >= 6:
            a.����б�.����(player.ID).��� -= 6
            a.����б�.����(player.ID).Ӣ�۳�.append('è')
            a.��Ϣ����.append(f"{player.ID} ���� 6 ��װ���ˡ�è��")
        else:
            a.��Ϣ����.append(f"{player.ID} �뻨�� 6 ��װ����è����������û��Ǯ��")
    UI.refresh(��Ϸ=a)
    client.kbdlistener.listen()



'''
version = '1.15'
client = ����()
client.start()
'''
