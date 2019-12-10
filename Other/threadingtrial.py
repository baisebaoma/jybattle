# coding=utf-8
import threading
import time


def chiHuoGuo(people):
    print("%s 吃火锅的小伙伴-羊肉：%s" % (time.ctime(), people))
    time.sleep(1)
    print("%s 吃火锅的小伙伴-鱼丸：%s" % (time.ctime(), people))


class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, people, name):
        '''重写threading.Thread初始化内容'''
        threading.Thread.__init__(self)
        self.threadName = name
        self.people = people

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        '''重写run方法'''
        print("开始线程: " + self.threadName)

        chiHuoGuo(self.people)  # 执行任务

        print("结束线程: " + self.name)


print("yoyo请小伙伴开始吃火锅：！！！")

# 创建新线程
thread1 = myThread("xiaoming", "Thread-1")
thread2 = myThread("xiaowang", "Thread-2")

# 守护线程setDaemon(True)
thread1.setDaemon(True)  # 必须在start之前
thread2.setDaemon(True)

# 开启线程
print('开始')
thread1.start()
thread2.start()

time.sleep(0.1)
print("退出主线程：吃火锅结束，结账走人")