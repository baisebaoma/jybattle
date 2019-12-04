import os


class UI:
    键盘监听 = None
    指针 = 0
    宽度 = 0
    高度 = 0
    """UI类负责所有的（文字版本的）UI绘制"""
    垂直同步 = True
    if 垂直同步:
        总输出 = ''

    @staticmethod
    def 翻译英雄池(列表):  # 打印列表
        if not 列表:
            return '无'
        字符串 = ''
        for 英雄 in 列表:
            字符串 += f'{英雄} '
        return 字符串[0:-1]  # 删掉最后一个空格

    @staticmethod
    def cls():
        os.system('cls')

    @classmethod
    def 长宽改变(cls):
        os.system('title 监狱威龙客户端（控制台版）')
        os.system(f'MODE con: COLS={cls.宽度} LINES={cls.高度}')

    @staticmethod
    def 汉字计数(内容):
        计数 = 0
        for 字 in 内容:
            if '\u4e00' <= 字 <= '\u9fa5':
                计数 += 1
        if 计数 % 2 == 1:
            计数 += 1
        return 计数

    @classmethod
    def 空格补齐(cls, 内容):
        return len(内容) + cls.汉字计数(内容)

    @classmethod
    def draw_line(cls, number=None, ID=None):
        if number and ID:
            cls.printc(f"-- {number} {ID} --")
        else:
            cls.printc("  ---------------------------------------------------  ")

    @classmethod
    def printc(cls, 内容, 居中=True):  # 全局控制居中输出，只要垂直同步是True 就会保存到总输出里
        总共计数 = len(内容)
        汉字计数 = cls.汉字计数(内容)
        空格数 = cls.宽度 // 2 - 总共计数 // 2 - 汉字计数 // 2
        if 空格数 < 0:
            空格数 = 0
        if not 居中:
            输出 = 内容
        else:
            输出 = ' ' * 空格数 + 内容
        if cls.垂直同步:
            if 内容 == '\n':
                cls.总输出 += '\n'
            else:
                cls.总输出 += 输出 + '\n'
        else:
            if 内容 == '\n':
                print()
            else:
                print(输出)

    @classmethod
    def draw_rank(cls, 游戏):
        rank = 1
        cls.draw_line()
        # cls.printc("排行榜")
        # cls.draw_line()
        # cls.draw_line()
        for 玩家 in 游戏.玩家列表:
            cls.draw_line(number=rank, ID=玩家.ID)
            cls.printc(f"【{玩家.角色}】")
            # print(' ' * 10 + str(玩家.角色))
            cls.printc(f"{玩家.金币}金币" + ' ' * 3 + \
                       f"{玩家.手牌}手牌" + ' ' * 3 + str(玩家.积分) + '积分')
            cls.printc(cls.翻译英雄池(玩家.英雄池))
            if rank != len(游戏.玩家列表):
                cls.printc('\n')
            rank += 1

    @classmethod
    def draw_message(cls, 游戏):
        cls.draw_line()
        # cls.printc("通告栏")
        # cls.draw_line()
        条数 = 5
        while len(游戏.消息队列) > 条数:
            del 游戏.消息队列[0]
        for 消息 in 游戏.消息队列:
            cls.printc(消息)
        if len(游戏.消息队列) < 条数:
            for i in range(1, 条数 + 1 - len(游戏.消息队列)):
                cls.printc('\n')

    @classmethod
    def draw_card(cls, 游戏):
        距离 = 5
        cls.draw_line()
        cls.printc(' ' * (cls.宽度 // 4 - 4) + "你的手牌：\n", 居中=False)
        if cls.键盘监听 == 'up' and cls.指针 > 0:
            cls.指针 -= 1
        if cls.键盘监听 == 'down' and cls.指针 < len(游戏.控制) - 1:
            cls.指针 += 1
        指针 = 0
        while 指针 < len(游戏.控制):
            if 指针 == cls.指针:
                cls.printc(' ' * (cls.宽度 // 4 - 3 - 距离) + ">>" + ' ' * 距离 + str(游戏.控制[指针]), 居中=False)
            else:
                cls.printc(' ' * (cls.宽度 // 4) + str(游戏.控制[指针]), 居中=False)
            指针 += 1

    @classmethod
    def draw_round(cls, 游戏):
        cls.printc(f"第{游戏.回合}回合")

    @classmethod
    def draw_control(cls, 游戏):
        cls.draw_line()
        # cls.printc("手牌区")
        # cls.draw_line()
        cls.draw_card(游戏)

    @classmethod
    def refresh(cls, 游戏):
        cls.cls()
        cls.draw_round(游戏)
        cls.draw_message(游戏)
        cls.draw_rank(游戏)
        cls.draw_card(游戏)
        if cls.垂直同步:
            # cls.cls()
            print(cls.总输出)
            cls.总输出 = ''
