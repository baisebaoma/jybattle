# -*- coding: utf-8 -*-
# import random
from client.kbdlistener import *
# from client.game import *
# from client.network import *
from client.UI import *
# from client.pygamemusic import *

# 别的都不用 import

# UIBase.垂直同步 = True
UIBase.宽度 = 55
UIBase.高度 = 60
UIBase.长宽改变()


'''
print("\033[31m这是红色字体\033[0m")
print("\033[32m这是绿色字体\033[0m")
print("\033[33m这是黄色字体\033[0m")
print("\033[34m这是蓝色字体\033[0m")
print("\033[38m这是默认字体\033[0m")
print("\033[7m这是默认红色字体背景绿色\033[0m")
'''

# 开始监听网络
# 网络.start()
# 开始监听键盘
# 键盘监听()

while True:
    UIController.search().draw()
    time.sleep(2)
