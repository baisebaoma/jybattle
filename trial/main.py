from scripts.player import *
import locale

# 每2秒收一次客户端发来的消息（告诉服务器我还在线，假如5秒内一直没收到那就将他视为掉线，一直保持接收他的消息，客户端一直尝试发送）

temp = os.system('title 监狱威龙')
temp = os.system('MODE con: COLS=50 LINES=30')

'''
print(" _____________ \n"
      "| BREAKMYWING |\n"
      "|             |\n"
      "|             |\n"
      "|             |\n"
      "|             |\n"
      "|             |\n"
      "|_____________|\n")
'''

# print(locale.getpreferredencoding(False))

s = Server()
s.start()

'''
login_username = input("用户名：")
login_password = input("密码：")
p.connect(login_username=login_username, login_password=login_username)
print(f"\n当前在线玩家：")
for player in p.player_list:
    if player.online:
        # print(player.login_username)
        player.rp = 10000
        print(f"{player.login_username} 的点券：{player.rp}")
'''

# p.player_list[p.find(f"{用户名}")].要改的数据 = 多少

# p.player_list[1].connect.send()

