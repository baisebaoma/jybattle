import random, socket

from dictionary import *


# ??????????????????
# ????????ID ??

# ?????? ???s
# ???tranlate??????????????


def input_better(word_to_print):
    while True:
        try:
            a = int(input(word_to_print))
            break
        except ValueError:
            print('[SERVER] ERROR!!!!!')


def score_count(player):
    global owned_cards
    c = 0
    for item in owned_cards[player]:
        c += card_score.get(item)
    return c


def translate_card(original_card_list):
    translated_list = []
    for item in original_card_list:  # ????????
        translated_list.append(card.get(item))
    return translated_list


def translate_champ(original_champ_list):
    translated_list = []
    for item in original_champ_list:  # ????????
        translated_list.append(champ.get(item))
    return translated_list


def translate_cost(original_card_list):
    translated_list = []
    for item in original_card_list:  # ??????cost
        translated_list.append(card_cost.get(item))
    return translated_list


def translate_score(original_card_list):
    translated_list = []
    for item in original_card_list:  # ????????
        translated_list.append(card_cost.get(item))
    return translated_list


def translate_color(original_card_list):
    translated_list = []
    for item in original_card_list:  # ????????
        translated_list.append(card_color.get(item))
    return translated_list


def translate_expla(original_card_list):
    translated_list = []
    for item in original_card_list:  # ????????
        translated_list.append(card_explanation.get(item))
    return translated_list


def getcard(player_to_get, card_to_get):
    global paidui
    global qipaidui
    global gold
    if paidui == [] or len(paidui) < card_to_get:
        print('[ERROR]????????????????????????')
        qipaidui += paidui
        paidui = recard(qipaidui)
    if paidui == [] or len(paidui) < card_to_get:
        print('[ERROR]??????????????????????2?')
        gold[player_to_get] += 2
        print(f'[SERVER] gold = {gold}')
        return
    i = 1
    while i <= card_to_get:
        shoupai[player_to_get].insert(0, paidui[0])
        paidui.remove(paidui[0])
        i += 1


def getcard1in2(player_to_get):
    global paidui
    global qipaidui
    if paidui == []:
        print('[ERROR]????????????????????????')
        qipaidui += paidui
        paidui = recard(qipaidui)
    if paidui == []:
        print('[ERROR]??????????????????????2?')
        gold[player_to_get] += 2
        print(f'[SERVER] ?? = {gold}')
        return
    control = int(input(f'[SERVER] ? ??{player_to_get} ? 1. {card[paidui[1]]} ? 2. {card[paidui[2]]} ???: '))
    if control == 1:
        shoupai[player_to_get].append(paidui[1])
        paidui.remove(paidui[1])
    elif control == 2:
        shoupai[player_to_get].append(paidui[2])
        paidui.remove(paidui[2])
    paidui.append(paidui[1])
    paidui.remove(paidui[1])


def recard(original_card_list):
    # ????????????????????
    random.shuffle(original_card_list)
    string_card_list = []
    return original_card_list


def playcard(player):
    global shoupai
    global owned_cards
    global gold
    global score
    print(f"""[SERVER] ?????{gold[player]}
[SERVER] ?????{translate_card(shoupai[player])}
[SERVER] ?????{translate_cost(shoupai[player])}
[SERVER] ?????{translate_color(shoupai[player])}""")
    good = False
    while not good:
        pai = int(input("[INPUT] ???????-1????0??????"))
        if pai != -1:
            if gold[player] >= card_cost.get(shoupai[player][pai]):
                gold[player] -= card_cost.get(shoupai[player][pai])
                owned_cards[player].append(shoupai[player][pai])
                shoupai[player].remove(shoupai[player][pai])
                print(f"""[SERVER] ?????{translate_card(shoupai[player])}
[SERVER] ???????{translate_card(owned_cards[player])}
[SERVER] ?????{score_count(player)}
[SERVER] ?????{gold[player]}""")
                score[player] = score_count(player)
                break
            else:
                print(f"[ERROR] ????")
                pass
        else:
            print(f"[SERVER] ???")
            break


def turn(champion_for_turn):  # ???player ?????
    '''
    check if killed
    show champion
    if constructions get extra gold
    choose whether get card or gold
    if constructor then up to 3 card
    if use card
    end
    '''
    global gold
    global shoupai
    global paidui

    player = from_champion_find_player(champion_for_turn)
    if player == -1:
        print(f"""
[SERVER] ????? {champ[champion_for_turn]}? ????????""")
        return
    print(f'''
[SERVER] ???? ?? {champ[champion_for_turn]} ?????''')
    if not if_killed[player]:
        print(f"[SERVER] ?? {champ[champion_for_turn]} ???? {player_ID[player]} (??{player}) ?")
        skillused = False
        actionbool = False
        while not skillused:
            action = int(input(f'[INPUT] ? {player_ID[player]} (??{player}) ??1???2??2???1???????3??????????? '))
            if action == 1:
                gold[player] += 2
                print(f'''[SERVER] {player_ID[player]} (??{player}) ?????2?
[SERVER] ?? = {gold}''')
                actionbool = True
                break
            elif action == 2:
                print(f'[SERVER] {player_ID[player]} (??{player}) ?????1?????????????')
                getcard1in2(player)
                print(f'''[SERVER] ?? = {translate_card(paidui)}
[SERVER] ?? = {translate_shoupai(shoupai)}
''')
                actionbool = True
                break
            elif action == 3:
                if if_used_skill[player]:
                    print("[ERROR] Skill used")
                else:
                    champion_skills(champion_for_turn)
                    if actionbool == True:
                        break
                # if if_used_skill[player]:
                    # break
        playcard(player)
        # ????8?????? ???end the game
        if max_card() >= 8:
            print(f"[SERVER] **********???????8???????????**********")
    else:
        print(f"""[SERVER] ??{champion_for_turn} ??????????????""")


def turn_controller():
    global player_number
    global if_killed
    global king

    i = 0  # i是英雄
    while True:
        while i < len(champ):
            turn(i)
            i += 1
        i = 0
        pick_champion(king)
        if_killed = [False for i in range(player_number)]


def max_card():
    global owned_cards
    global player_number
    a = len(owned_cards[0])
    for item in owned_cards:
        if len(item) >= a:
            a = len(item)
    return a


def champion_skills(champion):
    global if_used_skill
    global if_killed
    global gold
    global shoupai
    global king

    player = from_champion_find_player(champion)
    if champion == 0:  # ??
        kill = int(input("[INPUT] ?????????-1????"))
        if kill != -1:
            if kill != 0:
                if_killed[kill] = True
                print(f"[SERVER] ??? {champ[kill]}")
                if_used_skill[player] = True  # player??? ??????
            else:
                print(f"[ERROR] ???????")
        else:
            print(f"[SERVER] ???")

    elif champion == 1:  # ??
        kill = int(input("[INPUT] ?????????-1????"))
        if kill != -1:
            if kill != 1:
                gold[player] += gold[from_champion_find_player(kill)]
                gold[from_champion_find_player(kill)] = 0
                print(f"[SERVER] ??? {champ[kill]}")
                if_used_skill[player] = True  # player??? ??????
                print(f"[SERVER] gold = {gold}")
            else:
                print(f"[ERROR] ??????")
        else:
            print(f"[SERVER] ???")

    elif champion == 2:  # ???
        kill = int(input("[INPUT] ?????????-1????"))
        if kill != -1:
            if kill != 2:
                temp = shoupai[from_champion_find_player(kill)]
                shoupai[from_champion_find_player(kill)] = shoupai[player]
                shoupai[player] = temp
                print(f"[SERVER] ??? {champ[kill]}")
                if_used_skill[player] = True  # player??? ??????
                print(f"[SERVER] shoupai = {translate_shoupai(shoupai)}")
            else:
                print(f"[ERROR] ???????")
        else:
            print(f"[SERVER] ???")

    elif champion == 3:  # ??
        king = player
        print(f"""[SERVER] ?????????????
[SERVER] ???""")
        if_used_skill[player] = True  # player??? ??????

    elif champion == 4:  # ??
        print("[SERVER] ???????????")
        if_used_skill[player] = True  # player??? ??????
    else:
        print(f"[ERROR] ????" )


def pick_champion(king):
    global champion_pool
    global champion_selected
    global player_number

    champion_pool = list(range(0, 9))
    champion_selected = [-1 for i in range (player_number)]
    for item in first_loop(king):
        print(f'''
[SERVER] ???? player_ID[item] (??{item}) ????
[SERVER] ???: {champion_pool}
[SERVER] champion_selected: {champion_selected}''')
        champion_pick = int(input(f'''[INPUT] ? player_ID[item] (??{item}) ????????????'''))

        champion_pool.remove(champion_pick)
        champion_selected[item] = champion_pick
        print(f"[SERVER] player_ID[item] (??{item}) ???")


def first_loop(king):
    global player_number
    a = []
    i = king
    while len(a) < player_number:
        a.append(i)
        if i != player_number - 1:
            i += 1
        else:
            i = 0
    return a


def from_champion_find_player(champion):
    temp = 0
    for item in champion_selected:
        if champion_selected[temp] == champion:
            return temp
        else:
            temp += 1
    return -1  # ????? ??-1


def translate_shoupai(shoupai_for_translate):
    global player_number
    translated_list = [[] for temp in range(player_number)]
    i = 0
    for item in shoupai_for_translate:
        if item != []:
            for item2 in item:
                translated_list[i].insert(0, card.get(item2))
        i += 1
    return translated_list


def main():
    # ?? ????????x ??????-1
    # ??? ????
    # ???global???
    global if_used_skill
    global player_number
    global gold
    global if_killed
    global shoupai
    global paidui
    global qipaidui
    global champion_pool
    global champion_selected
    global king
    global owned_cards
    global score

    player_number = 8  # ????
    gold = [2 for i in range(player_number)]  # ?????
    if_killed = [False for i in range(player_number)]  # ???????
    shoupai = [[] for i in range(player_number)]  # ?????
    paidui = recard(list(range(1, len(card))))  # ?????(?1??)
    qipaidui = []  # ??????
    champion_pool = list(range(0, 9))  # ??????(?0??)
    champion_selected = [3, 0, 2, 5, 1, 4, 7, 6]  # ????
    if_used_skill = [False for i in range(player_number)]
    # first = [False for i in range(player_number)]  # ????????
    # first[random.randint(0, player_number-1)] = True  # ???? ??? ?-1
    getcardvariable = 0  # ???2??
    while getcardvariable < player_number:
        getcard(getcardvariable, 2)
        getcardvariable += 1
    owned_cards = [[] for i in range(player_number)]
    score = [0 for i in range(player_number)]
    king = from_champion_find_player(3)
    player_ID[0] = 'WTF BreakMyWing'
    player_ID[1] = 'WTF Raging'
    player_ID[2] = 'WTF Imperator'
    player_ID[3] = 'WTF HeartBreak'
    player_ID[4] = 'WTF KoKou'
    player_ID[5] = 'zackshang1213'
    player_ID[6] = 'cbt321'
    player_ID[7] = 'WTF Sparrow'
    print(f"""
[SERVER] ??? ???? = {player_number} ??
[SERVER] ??? ?? = {gold} ??
[SERVER] ??? ?????? = {if_killed} ??
[SERVER] ??? ?? = {translate_shoupai(shoupai)} ??
[SERVER] ??? ?? = {translate_card(paidui)} ??
[SERVER] ??? ??? = {champion_pool} ??
[SERVER] ??? ??? = {translate_card(qipaidui)} ??
[SERVER] ??? (?????)???? = {translate_champ(champion_selected)} ??
""")
    turn_controller()


def network():
    pass


main()
