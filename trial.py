import webbrowser
import threading


def browse():
    webbrowser.open("http://www.baidu.com")


thread = threading.Thread(target=browse)
thread.start()
