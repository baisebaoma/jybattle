import random

'''
class 角色:
    class 角色:
        pass

    class 排位:
        结果 = False
        pass

    class ZER(角色):
        @classmethod
        def 技能(cls, 自己, 对象, 回合数):
            胜率 = 0
            擅长英雄个数 = 0
            for 英雄 in 自己.英雄池:
                if 英雄 in ["Xayah", "Ryze", "Fiora", "Akali", "Kai'Sa"]:
                    擅长英雄个数 += 1
            胜率字典 = {
                0: 0.1,
                1: 0.2,
                2: 0.4,
                3: 0.6,
                4: 0.9,
                5: 1.0
            }
            胜率 = 胜率字典[擅长英雄个数]
            随机数 = random.random()  # 生成一个在 [0,1) 的数
            结果 = True if 随机数 <= 胜率 else False
            if 结果:
                第一个人分牌数 = random.randint(0, 回合数)
                第二个人分牌数 = 回合数 - 第一个人分牌数
                自己.手牌数 += 第一个人分牌数
                对象.手牌数 += 第二个人分牌数
            else:
                对象.手牌数 = -100  # 爷心态崩了
            print(胜率, 随机数, 结果)


回合数 = 3


class 玩家:
    手牌数 = 0
    英雄池 = list()

    def __init__(self, 手牌数, 英雄池):
        self.手牌数 = 手牌数
        self.英雄池 = 英雄池


自己 = 玩家(0, ["Xayah", "Ryze"])
对象 = 玩家(0, list())

print(自己.英雄池)

角色.ZER.技能(自己, 对象, 回合数)

print(自己.手牌数, 对象.手牌数)
'''


class 角色:
    class 排位:
        结果 = False
        pass

    class 角色:
        @staticmethod
        def 概率(英雄池, 名字列表, 概率字典):
            擅长英雄个数 = 0
            for 英雄 in 英雄池:
                if 英雄.名字 in 名字列表:
                    擅长英雄个数 += 1
            胜率 = 概率字典[擅长英雄个数]
            print(胜率)
            随机数 = random.random()  # 生成一个在 [0,1) 的数
            print(随机数)
            结果 = True if 随机数 <= 胜率 else False
            print(结果)
            return 结果

    class ZER(角色):
        @classmethod
        def 技能(cls, 自己, 对象, 回合数):
            # 对象 是玩家，不是角色！
            概率字典 = {
                0: 0.1,
                1: 0.2,
                2: 0.4,
                3: 0.6,
                4: 0.9,
                5: 1.0
            }
            结果 = cls.概率(自己.英雄池, ["Xayah", "Ryze", "Fiora", "Akali", "Kai'Sa"], 概率字典)
            if 结果:
                第一个人分牌数 = random.randint(0, 回合数)
                第二个人分牌数 = 回合数 - 第一个人分牌数
                自己.手牌数 += 第一个人分牌数
                对象.手牌数 += 第二个人分牌数
                return [True, 第一个人分牌数, 第二个人分牌数]
            else:
                对象.手牌数 = -100  # 爷心态崩了
                return [False]
            # print(胜率, 随机数, 结果)

    class ZXX(角色):
        @classmethod
        def 技能(cls, 自己, 对象, 属性):
            # 对象 是玩家，不是角色！
            # 属性 1 = 偷全部钱， 2 = 偷指定玩家钱
            # return [True, 属性]
            if 属性 == 1:
                对象.被偷钱 = True
                return [True, 1]
            elif 属性 == 2:
                擅长英雄个数 = 0
                for 英雄 in 自己.英雄池:
                    if 英雄.名字 in ["Nautilus", "Blitz", "Lee Sin"]:
                        擅长英雄个数 += 1
                掠夺字典 = {
                    0: 0,
                    1: 1,
                    2: 3,
                    3: 7
                }
                掠夺 = 掠夺字典[擅长英雄个数]
                自己.金币 += 掠夺
                对象.金币 -= 掠夺
                return [True, 2]
            return [False, 0]

    class ZHL(角色):
        @staticmethod
        def 技能(自己, 对象):
            # 对象 是玩家，不是角色！
            # return [True] if success
            # 擅长英雄个数 = 0
            掠夺 = 2
            对象.被换牌 = True
            for 英雄 in 自己.英雄池:
                if 英雄.名字 in ["Gangplank"]:
                    自己.金币 += 掠夺
                    对象.金币 -= 掠夺
            return [True]

    class SKL(角色):
        @classmethod
        def 技能(cls, 自己, 玩家列表):
            # 对象 是玩家，不是角色！
            概率字典 = {
                0: 0.3,
                1: 0.4,
                2: 0.5,
                3: 0.5,
                4: 1.0,
            }
            结果 = cls.概率(自己.英雄池, ["Ashe", "Ezreal", "Yasuo", "Kai'Sa"], 概率字典)
            if 结果:
                for 玩家 in 玩家列表:
                    玩家.金币 -= 1
                    自己.金币 += 1
                return [True]
            else:
                return [False]
            # print(胜率, 随机数, 结果)

    class XJB:
        @classmethod
        def 技能(cls, 自己, 玩家列表):
            # 对象 是玩家，不是角色！
            pass


if __name__ == '__main__':

    # 测试用
    class 玩家:
        金币 = 0
        手牌 = list()
        英雄池 = list()
        准备 = False
        跳回合 = False
        手牌数 = 0

        def __init__(self, 用户名='', 连接=None):
            self.用户名 = 用户名
            self.连接 = 连接


    class 英雄:
        def __init__(self, 名字=''):
            self.名字 = 名字


    自己 = 玩家()
    自己.英雄池 = [英雄("Xayah"), 英雄("Ryze"), 英雄("Blitz"), 英雄("Nautilus"), 英雄("Lee Sin")]
    自己.手牌 = 0
    对象 = 玩家()
    对象.英雄池 = [英雄("Xayah"), 英雄("Ryze")]
    对象.手牌 = 0

    玩家列表 = list()
    玩家列表.append(自己)
    玩家列表.append(对象)

    # 角色.ZER.技能(自己, 对象, 3)
    角色.SKL.技能(自己, 玩家列表)

    print(自己.金币, 对象.金币)

