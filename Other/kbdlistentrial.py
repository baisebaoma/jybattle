
import msvcrt
import threading

import msvcrt

def listen_thread():
    while True:
        e = ord(msvcrt.getch())
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
        else:
            print(e)
            print(type(e))
            print(type(72))


def listen():
    thread = threading.Thread(target=listen_thread())
    thread.start()


if __name__ == '__main__':
    listen_thread()


'''
import keyboard #Using module keyboard
while True:#making a loop
    try: #used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('q'):#if key 'q' is pressed
            print('You Pressed A Key!')
            break#finishing the loop
        else:
            pass
    except:
        break #if user pressed other than the given key the loop will break
'''

'''
import msvcrt
while True:
    print(ord(msvcrt.getch()))
    print('you pressed a button')
'''
