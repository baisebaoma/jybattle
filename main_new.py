from scripts.player_new_zh_CN import *
import os

# import locale

# 每2秒收一次客户端发来的消息（告诉服务器我还在线，假如5秒内一直没收到那就将他视为掉线，一直保持接收他的消息，客户端一直尝试发送）

temp = os.system('title 监狱威龙服务器')
temp = os.system('MODE con: COLS=50 LINES=30')

# print(locale.getpreferredencoding(False))

Server.start()

# p.player_list[p.find(f"{用户名}")].要改的数据 = 多少

# p.player_list[1].connect.send()

