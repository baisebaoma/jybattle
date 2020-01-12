class Nihao:
    @classmethod
    def __nihao(cls):
        print("nihao")


class Nihao2(Nihao):
    @classmethod
    def nihao(cls):
        cls.__nihao()


Nihao2.nihao()
