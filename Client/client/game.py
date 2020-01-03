class 玩家:
    def __init__(self, ID):
        self.ID = ID
        self.金币 = 0
        self.角色 = None  # None = 未公布
        self.英雄池 = list()
        self.手牌 = 0  # 对于别的玩家，只能看到手牌数但是不能看到几张牌
        self.积分 = 0


class 游戏:
    class 玩家列表类(list):
        def __init__(self, *args):
            super().__init__(*args)

        def 搜索(self, ID):
            for 玩家 in self:
                if 玩家.ID == ID:
                    return 玩家
    房间名 = '' + '的房间'
    玩家列表 = 玩家列表类()
    消息队列 = list()
    输入 = None
    控制 = list()
    手牌 = list()
    回合 = 1
    允许操作 = True

