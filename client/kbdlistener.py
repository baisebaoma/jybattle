from pynput import keyboard
from client.UI import UI


def on_press(key):
    pass


def on_release(key):
    if key == keyboard.Key.left:
        UI.键盘监听 = 'left'
        return False
    if key == keyboard.Key.right:
        UI.键盘监听 = 'right'
        return False
    if key == keyboard.Key.up:
        UI.键盘监听 = 'up'
        return False
    if key == keyboard.Key.down:
        UI.键盘监听 = 'down'
        return False
    if key == keyboard.Key.enter:
        UI.键盘监听 = 'enter'
        return False
    if key == keyboard.Key.space:
        UI.键盘监听 = 'space'
        return False


    # if key == Key.esc:  # 停止监听
    #     return False


def listen():
    with keyboard.Listener(on_press=None, on_release=on_release) as listener:
        listener.join()


if __name__ == '__main__':
    listen()
