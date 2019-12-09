from pynput import keyboard
from client.UI import *
# from client.UI import UI
import time


def on_press(key):
    pass


def on_release(key):

    if key == keyboard.Key.left:
        UI.键盘监听 = 'left'
        refresh()
    elif key == keyboard.Key.right:
        UI.键盘监听 = 'right'
        refresh()
    elif key == keyboard.Key.up:
        UI.键盘监听 = 'up'
        refresh()
    elif key == keyboard.Key.down:
        UI.键盘监听 = 'down'
        refresh()
    elif key == keyboard.Key.enter:
        UI.键盘监听 = 'enter'
        refresh()
    elif key == keyboard.Key.space:
        UI.键盘监听 = 'space'
        refresh()


def refresh():
    if UI.busy is False:
        UI.refresh()
    else:
        while UI.busy is True:
            time.sleep(0.1)
        UI.refresh()
# return False 就可以结束


def listen():
    '''
    with keyboard.Listener(on_press=None, on_release=on_release) as listener:
        listener.wait()
    print(keyboard.Listener(on_press=None, on_release=on_release).isDaemon())
    '''
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()


if __name__ == '__main__':
    listen()
