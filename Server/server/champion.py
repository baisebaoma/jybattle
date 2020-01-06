class 英雄:
    class 英雄:
        名字 = ''
        金币 = 0

    class 霞(英雄):
        名字 = "Xayah"
        金币 = 3

    class 瑞兹(英雄):
        名字 = "Ryze"
        金币 = 2

    class 菲奥娜(英雄):
        名字 = "Fiora"
        金币 = 3

    class 阿卡丽(英雄):
        名字 = "Akali"
        金币 = 3

    class 卡莎(英雄):
        名字 = "Kai'Sa"
        金币 = 3

    class 诺提勒斯(英雄):
        名字 = "Nautilus"
        金币 = 2

    class 布里茨(英雄):
        名字 = "Blitz"
        金币 = 5

    class 李青(英雄):
        名字 = "Lee Sin"
        金币 = 10

    class 普朗克(英雄):
        名字 = "Gangplank"
        金币 = 6

    class 艾希(英雄):
        名字 = "Ashe"
        金币 = 4

    class 伊泽瑞尔(英雄):
        名字 = "Ezreal"
        金币 = 9

    class 泽拉斯(英雄):
        名字 = "Xerath"
        金币 = 14

    class 布兰德(英雄):
        名字 = "Brand"
        金币 = 3

    class 锤石(英雄):
        名字 = "Thresh"
        金币 = 10

    class 阿狸(英雄):
        名字 = "Ahri"
        金币 = 6

    class 亚索(英雄):
        名字 = "Yasuo"
        金币 = 10

    class 易大师(英雄):
        名字 = "Yi"
        金币 = 2


if __name__ == "__main__":
    牌堆 = list()
    for 类 in 英雄.英雄.__subclasses__():
        牌堆.append(类())
    print(牌堆)
