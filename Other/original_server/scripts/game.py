import random
import scripts.player_new

# 先暂时用？？表示询问玩家是否

# 区分：champion 表示 英雄，character 表示角色，player 表示玩家！！


class Chars:
    def skill(self):
        pass

class Zer(Chars):
    pass


class Game:
    def __init__(self, player_list):
        self.player_list = player_list  # player_list 是包含了的玩家！
        self.player = len(player_list)  # player 是人数！

    def __assign(self):
        pass

    def __game_start(self):
        for player in self.player_list:
            player.send("")






a = Game(['nihao', 'nihao', 'nihao'])
print(a.player)
