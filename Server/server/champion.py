import random

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
        金币 = 7

    class 卡莎(英雄):
        名字 = "Kai'Sa"
        金币 = 5

    class 诺提勒斯(英雄):
        名字 = "Nautilus"
        金币 = 4

    class 布里茨(英雄):
        名字 = "Blitz"
        金币 = 5

    class 李青(英雄):
        名字 = "Lee Sin"
        金币 = 9

    class 普朗克(英雄):
        名字 = "Gangplank"
        金币 = 6

    class 艾希(英雄):
        名字 = "Ashe"
        金币 = 2

    class 伊泽瑞尔(英雄):
        名字 = "Ezreal"
        金币 = 4

    class 泽拉斯(英雄):
        名字 = "Xerath"
        金币 = 6

    class 布兰德(英雄):
        名字 = "Brand"
        金币 = 3

    class 锤石(英雄):
        名字 = "Thresh"
        金币 = 8

    class 阿狸(英雄):
        名字 = "Ahri"
        金币 = 6

    class 亚索(英雄):
        名字 = "Yasuo"
        金币 = 10

    class 易大师(英雄):
        名字 = "Yi"
        金币 = 2

    class 盖伦(英雄):
        名字 = "Garen"
        金币 = 1

    class 德莱厄斯(英雄):
        名字 = "Darius"
        金币 = 1

    class 德莱文(英雄):
        名字 = "Draven"
        金币 = 7

    class 卡特琳娜(英雄):
        名字 = "Katarina"
        金币 = 7

    class 锐雯(英雄):
        名字 = "Riven"
        金币 = 10

    class 沃里克(英雄):
        名字 = "Warwick"
        金币 = 1

    class 娑娜(英雄):
        名字 = "Sona"
        金币 = 1

    class 派克(英雄):
        名字 = "Pyke"
        金币 = 7

    class 厄斐琉斯(英雄):
        名字 = "Aphelios"
        金币 = 14

    class 吉格斯(英雄):
        名字 = "Ziggs"
        金币 = 4

    class 劫(英雄):
        名字 = "Zed"
        金币 = 8

    class 悠米(英雄):
        名字 = "Yuumi"
        金币 = 2

    class 薇恩(英雄):
        名字 = "Vayne"
        金币 = 9

    class 蒙多(英雄):
        名字 = "Mundo"
        金币 = 2

    class 约里克(英雄):
        名字 = "Yorick"
        金币 = 1

    class 拉克丝(英雄):
        名字 = "Lux"
        金币 = 2

    class 妮蔻(英雄):
        名字 = "Neeko"
        金币 = 3

    class 索拉卡(英雄):
        名字 = "Soraka"
        金币 = 1

    class 弗拉基米尔(英雄):
        名字 = "Vladimir"
        金币 = 2

    class 茂凯(英雄):
        名字 = "Maokai"
        金币 = 1

    class 奥拉夫(英雄):
        名字 = "Olaf"
        金币 = 5

    class 卢锡安(英雄):
        名字 = "Lucian"
        金币 = 5

    class 墨菲特(英雄):
        名字 = "Malphite"
        金币 = 1

    class 佐伊(英雄):
        名字 = "Zoe"
        金币 = 8


if __name__ == "__main__":
    '''
    牌堆 = list()
    for 类 in 英雄.英雄.__subclasses__():
        牌堆.append(类())
    print(牌堆)
    '''
    all_cards = [[] for i in range(15)]
    for cls in 英雄.英雄.__subclasses__():
        all_cards[int(cls.金币)].append(cls.__name__)
        # all_cards[int(cls.金币)].append('*')
    for x in range(15):
        print(f"{x}费卡 {len(all_cards[x])}张 {all_cards[x]}")
    print()
    牌堆 = list()
    for 类 in 英雄.英雄.__subclasses__():
        if 类.金币 >= 7:
            for x in range(1):
                牌堆.append(类.__name__)

        elif 类.金币 >= 5:
            for x in range(3):
                牌堆.append(类.__name__)

        elif 类.金币 >= 1:
            for x in range(4):
                牌堆.append(类.__name__)

    random.shuffle(牌堆)
    for 牌 in 牌堆:
        print(牌)
