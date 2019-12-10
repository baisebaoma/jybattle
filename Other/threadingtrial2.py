import threading
import msvcrt
import time


def listen_thread():
    while True:
        print(100)
        time.sleep(1)


'''        e = ord(msvcrt.getch())
        if e == 224:
            e2 = ord(msvcrt.getch())
            if e2 == 72:
                print('up')
            elif e2 == 80:
                print('down')
            elif e2 == 75:
                print('left')
            elif e2 == 77:
                print('right')
        elif e == 13:
            print('enter')
        else:
            pass'''

def listen():
    print('创建线程')
    线程 = threading.Thread(target=listen_thread, args=())
    print('设置子线程')
    线程.setDaemon(True)
    线程.run()
    return

# 我晓得了 不要括号

if __name__ == '__main__':
    listen()

