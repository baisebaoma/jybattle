import client.UI
import client.game
import threading
import msvcrt
import time

def listen_thread():
    while True:
        e = ord(msvcrt.getch())
        if e == 224:
            e2 = ord(msvcrt.getch())
            if e2 == 72:
                client.UI.UI.键盘监听 = 'up'
            elif e2 == 80:
                client.UI.UI.键盘监听 = 'down'
            elif e2 == 75:
                client.UI.UI.键盘监听 = 'left'
            elif e2 == 77:
                client.UI.UI.键盘监听 = 'right'
            client.UI.UI.refresh()
        elif e == 13:
            if client.game.游戏.允许操作:
                client.UI.UI.键盘监听 = 'enter'
                client.UI.UI.refresh()
        else:
            pass
        time.sleep(0.13)


def listen():
    print('创建线程')
    线程 = threading.Thread(target=listen_thread)
    print('设置子线程')
    线程.setDaemon(True)
    线程.start()
    return

'''
if __name__ == '__main__':
    listen_thread()
'''
