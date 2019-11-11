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
p = PlayerController()
s = Server()
s.start()


login_username = input("用户名：")
login_password = input("密码：")
p.connect(login_username=login_username, login_password=login_username)
print(f"\n当前在线玩家：")
for player in p.player_list:
    if player.online:
        # print(player.login_username)
        player.rp = 10000
        print(f"{player.login_username} 的点券：{player.rp}")

# p.player_list[p.find(f"{用户名}")].要改的数据 = 多少

# p.player_list[1].connect.send()

'''
# 真的吗？？这真的是最折衷的方案？
# 我可以写一个 用户名list 然后..?
# 要发送信息：printp("信息","用户名")，让这个函数去找用户名在哪里
# 要修改数据：change("用户名", "数据", "值")change
'''

'''
n = 0
while True:
    print(f"n = {n}")
    i = int(input("1 登录，2 注册："))
    if i == 2:
        try:
            p.player_list[n].sign_up()
        except IndexError:
            p.player_list.append(Player())
            p.player_list[n].sign_up()
    elif i == 1:
        p.connect(n)
        print(f"\n当前在线玩家：")
        for player in p.player_list:
            # if player.online:
            print(player.login_username)
    n += 1
'''
'''
i = int(input("1 登录，2 注册："))
if i == 2:
    p.player_online[0].sign_up()
elif i == 1:
    p.connect(0)
    print("当前在线玩家：")
    for player in p.player_online:
        print(player.login_username)
'''

# p.disconnect(0)

'''
def connect(x):
    # if found someone connected
    player_online[x].login()
    print(player_online[0].login_username)


def disconnect(x):
    player_online[x].online = False
    # if found someone disconnected numbered x
    # del player_online[0]
'''

'''
player = [0, 1, 2, 3, 4, 5, 6]
print(player)
del player[3]
print(player)
'''
