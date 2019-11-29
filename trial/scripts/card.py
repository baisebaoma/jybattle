class Card:
    cost = 0
    skill = False
    bonus = list()

    def learn(self):
        self.bonus.append('CBT')

    def buy(self, tgt):
        if tgt.gold >= self.cost:
            tgt.gold -= self.cost
            tgt.field.append(self)
            tgt.card.remove(self)
            return 0
        else:
            return -1


class Xerath(Card):
    pass

# card_list = [Blitz()] * 3 + [Nautilus()] * 100



class Game:
    class Player:
        def __init__(self):
            self.gold = 0
            self.field = list()
            self.card = list()

        def get_card(self, 牌堆):
