# 1. At any stage of the game if you do not have a suitable card please type none  !!
# 2. At any stage of the game if you need help and to read the rules of the game please type --help when it's
#    your time to choose card and when you done type --resume.
# 3. When you want to finish card or super taki pleas insert close
# 4. This play fit the regular game and not the TAKI PYRAMID TOURNAMENT

import random
import webbrowser
import cards

STEP_STAY_CURRENT_PLAYER = 0
STEP_MOVE_FORWARD = 1
STEP_SKIP_NEXT = 2
STEP_MOVE_BACKWARD = -1
AVAILABLE_COLORS = ['g', 'y', 'r', 'b']


def helper():
    webbrowser.open('https://www.takigame.com/taki-game-rules')


def handle_user_input(msg):
    user_input = input(msg)
    if user_input == "--help":
        helper()
        return handle_user_input(msg)
    return user_input


def sets_players():
    num_players = int(handle_user_input("How many players are interested in playing? "))
    while num_players < 2 or num_players > 4:
        print("This game can be played by 2 to 4 players ")
        num_players = int(handle_user_input("Please enter the number of players again: "))
    list_players = []
    while len(list_players) < num_players:
        name = handle_user_input("Please enter your name: ")
        flag = True
        while flag:
            if name in list_players:
                answer = handle_user_input("{} is already in the list name are you sure you want to players to"
                                           " have the same name [y/n]?".format(name))
                if answer == 'y':
                    list_players.append(name)
                    flag = False
                else:
                    name = handle_user_input("Please enter your name: ")
            else:
                list_players.append(name)
                flag = False
    return list_players, num_players


def generate_cards_deck():
    deck = ['color_changer'] * 4 + [cards.SUPER_TAKI] * 2 + ['king'] * 2 + ['plus3'] * 2 + ['break3'] * 2
    special_card = ['stop', 'change_direction', 'plus', 'taki']
    for i in range(1, 10):
        for j in range(len(AVAILABLE_COLORS)):
            deck.extend([str(i) + '_' + AVAILABLE_COLORS[j]] * 2)
    for i in range(len(special_card)):
        for j in range(len(AVAILABLE_COLORS)):
            deck.extend([special_card[i] + '_' + AVAILABLE_COLORS[j]] * 2)
    return random.sample(deck, len(deck))


def game_boot(cards, num_players):
    players_cards = [[] for x in range(num_players)]
    counter = 0
    while counter < 8:
        for i in range(number_of_players):
            players_cards[i].append(cards[0])
            del cards[0]
        counter += 1
    return cards, players_cards


def card_rule(card, color):
    if card[0:4] == 'stop':
        current_step = STEP_SKIP_NEXT
        new_color = card[-1]
    elif card[0:-2] == 'change_direction':
        current_step = STEP_MOVE_BACKWARD
        new_color = card[-1]
    elif card == 'plus3' or card == 'break3':
        current_step = STEP_MOVE_FORWARD
        new_color = color
    elif card[0:4] == 'plus' or card[0:4] == 'taki':
        current_step = STEP_STAY_CURRENT_PLAYER
        new_color = card[-1]
    elif card == cards.SUPER_TAKI or card == 'color_changer':
        if card == cards.SUPER_TAKI:
            current_step = STEP_STAY_CURRENT_PLAYER
        else:
            current_step = STEP_MOVE_FORWARD
        new_color = None
        while new_color not in AVAILABLE_COLORS:
            if new_color is not None:
                print("The color \"{}\" is not available, here are your options: {}".
                      format(new_color, AVAILABLE_COLORS))
            new_color = handle_user_input('Please choose the color you want: ')
    elif card == 'king':
        current_step = STEP_STAY_CURRENT_PLAYER
        new_color = color
    else:
        current_step = 1
        new_color = card[-1]
    return current_step, new_color


def checking_legality(used_card, current_card, color):
    if used_card[0] == 'done':
        if len(used_card) > 1 and used_card[1][0] == '2':
            if current_card[0] == '2' or current_card == 'king':
                return False
            elif current_card[-1] == color or current_card == cards.SUPER_TAKI or \
                    current_card == 'color_changer' or current_card == 'king':
                return False
        elif len(used_card) > 1 and (used_card[1][0] == 'plus3' or used_card[1][0] == 'break3'):
            if current_card[-1] == color or current_card == cards.SUPER_TAKI or \
                    current_card == 'color_changer' or current_card == 'king':
                return False
        else:
            print("You choose an invalid card! If you don't have valid card please type 'none'. ")
            return True
    elif used_card[0][0].isnumeric():
        if used_card[0][0] == current_card[0] or used_card[0][-1] == current_card[-1] or \
                current_card == cards.SUPER_TAKI or current_card == 'color_changer' or current_card == 'king' or \
                current_card == 'plus3' or current_card == 'break3':
            return False
        else:
            print("You choose an invalid card! If you don't have valid card please type 'none'. ")
            return True
    elif used_card[0][-2] == '_':
        if used_card[0][-1] == current_card[-1]:
            return False
        elif used_card[0][0:-2] == current_card[0:-2]:
            return False
        elif current_card == '' or current_card == 'color_changer' or current_card == 'king' or \
                current_card == 'plus3' or current_card == 'break3':
            return False
        else:
            print("You choose an invalid card! If you don't have valid card please type 'none'. ")
            return True
    elif used_card[0] == 'color_changer':
        if current_card[-1] == color or current_card == cards.SUPER_TAKI or current_card == 'king' or \
                current_card == 'plus3' or current_card == 'break3':
            return False
        else:
            print("You choose an invalid card! If you don't have valid card please type 'none'. ")
            return True
    elif current_card == 'king':
        return False
    elif current_card == 'break3':
        if current_card[-1] == color or current_card == cards.SUPER_TAKI or current_card == 'king' or \
                current_card == 'plus3' or current_card == 'color_changer':
            return False
    else:
        print("You choose an invalid card! If you don't have valid card please type 'none'. ")
        return True


def plus2(used_card, cards_deck):
    if used_card[0][0] == '2':
        count = 0
        for i in range(len(used_card)):
            if used_card[i][0] == '2':
                count += 2
            else:
                break
        while count > 0:
            players_cards[current_player].append(cards_deck[0])
            del cards_deck[0]
            count -= 1
        used_card.insert(0, 'done')
    else:
        players_cards[current_player].append(cards_deck[0])
        del cards_deck[0]
    return players_cards, cards_deck


def plus3(players, players_cards, current_player , used_card, cards_deck):
    player = handle_user_input('if you have break3 card please enter your name if no one have break3 enter none: ')
    if player == 'none':
        for i in range(0, 3):
            for j in range(len(players)):
                if players[j] != players[current_player]:
                    players_cards[j].append(cards_deck[0])
                    del cards_deck[0]
    else:
        del players_cards[players.index(player)][players_cards[players.index(player)].index('break3')]
        used_card.insert(0, 'break3')
        for i in range(0, 3):
            players_cards[current_player].append(cards_deck[0])
            del cards_deck[0]
    used_card.insert(0, 'done')
    return used_card, players_cards, cards_deck


def step_zero_case(used_card, players_cards, current_player, card, cards_deck, step, color):
    if card[0:4] == 'plus':
        new_card = handle_user_input('please choose card again: ')
        if new_card[0:4] == 'plus':
            used_card.insert(0, new_card)
            del players_cards[current_player][players_cards[current_player].index(new_card)]
            card = new_card
            used_card, players_cards, current_step, cards_deck, new_color = step_zero_case(used_card, players_cards,
                                                                                           current_player, card,
                                                                                           cards_deck, step, color)
            return used_card, players_cards, current_step, cards_deck, new_color
        elif new_card == 'none':
            players_cards[current_player].append(cards_deck[0])
            del cards_deck[0]
            current_step = step
            return used_card, players_cards, current_step, cards_deck, color
        else:
            flag = True
            while flag:
                flag = checking_legality(used_card, card, color)
                if flag == True:
                    new_card = handle_user_input('please choose card again: ')
            used_card.insert(0, new_card)
            del players_cards[current_player][players_cards[current_player].index(new_card)]
            card = new_card
            current_step, color = card_rule(card, color)
            return used_card, players_cards, current_step, cards_deck, color

    elif card == 'king':
        new_card = handle_user_input('please choose card again: ')
        if new_card == 'king':
            used_card, players_cards, current_step, cards_deck, new_color = step_zero_case(used_card, players_cards,
                                                                                           current_player, card,
                                                                                           cards_deck, step, color)
            return used_card, players_cards, current_step, cards_deck, new_color
        else:
            current_step, color = card_rule(new_card, color)
            del players_cards[current_player][players_cards[current_player].index(new_card)]
            used_card.insert(0, new_card)
            return used_card, players_cards, current_step, cards_deck, color

    else:  # taki/super_taki
        if card[0:4] == 'taki':
            new_color = card[-1]
        if card[6:11] == 'taki':
            new_color =color
        status = 'continue'
        while status != 'stop':
            flag = True
            while flag:
                new_card = handle_user_input('please choose card again: ')
                if new_card == 'none':
                    status = 'stop'
                    flag = False
                    new_card = 'close'
                    current_step = step
                elif new_card != 'close':
                    flag = checking_legality(used_card, card, new_color)
                else:
                    status = 'stop'
                    flag = False
                    current_step = step
            if new_card != 'close':
                card = new_card
                used_card.insert(0, new_card)
                del players_cards[current_player][players_cards[current_player].index(card)]
                current_step, new_color = card_rule(new_card, color)
        while current_step == STEP_STAY_CURRENT_PLAYER:
            used_card, players_cards, current_step, cards_deck, new_color = step_zero_case(used_card, card, step, color)
            return used_card, players_cards, current_step, cards_deck, new_color
        return used_card, players_cards, current_step, cards_deck, new_color


def play(players, current_player, step, players_cards, cards_deck, used_card, color):
    # checking legality of the move & the option the players don't have any move to do
    print("It's " + players[current_player] + ' turn')
    print('your hand is: ', end='')
    print(players_cards[current_player])
    if used_card[0] == 'done':
        if used_card[1][0] == '2':
            print('the current card is ' + used_card[1])
            print('But someone has already been punished for not putting a card of 2! and the color is ', color)
        elif used_card[1] == 'break3':
            print('the current card is ' + used_card[1])
            print('But someone has already been punished for not putting a card of break3! and the color is ', color)
        else:
            print('the current card is ' + used_card[1])
            print('But someone has already been punished for not putting a card of plus3! and the color is ', color)

    else:
        print('the current card is ' + used_card[0])
        if used_card[0][-2] != '_':
            print('The color is ', color)
    flag = True
    while flag:
        current_card = handle_user_input(players[current_player] + ' please choose a card: ')
        if current_card == 'none':
            break
        else:
            if current_card in players_cards[current_player]:
                flag = checking_legality(used_card, current_card, color)
            else:
                print('The card you selected does not exist in your deck')
    if current_card == 'none':
        players_cards, cards_deck = plus2(used_card, cards_deck)
        current_step = step
    elif used_card[0] == 'done':
        del used_card[0]
        used_card.insert(0, current_card)
        current_step, color = card_rule(current_card, color)
    else:
        del players_cards[current_player][players_cards[current_player].index(current_card)]
        used_card.insert(0, current_card)
        current_step, color = card_rule(current_card, color)

    # checking the option that the current player won
    if len(players_cards[current_player]) == 0:
        if current_card[0:4] == 'plus':
            players_cards[current_player].append(cards_deck[0])
            del cards_deck[0]
        elif current_card == 'break3':
            if used_card[1] == 'plus3':
                return False, current_player, 0, players_cards, cards_deck, used_card, color
            else:
                players_cards[current_player].extend(cards_deck[0:3])
                del cards_deck[0:3]
        else:
            return False, current_player, 0, players_cards, cards_deck, used_card, color

    # plus3 case
    if current_card == 'plus3':
        used_card, players_cards, cards_deck = plus3(players, players_cards, current_player, used_card, cards_deck)
    if current_card == 'break3':
        for i in range(0, 3):
            players_cards[current_player].append(cards_deck[0])
            del cards_deck[0]

    # zero step cases (taki,plus,super_taki,king)
    if current_step == 0:
        used_card, players_cards, current_step, cards_deck, color = step_zero_case(used_card, players_cards,
                                                                                   current_player, current_card,
                                                                                   cards_deck, step, color)
    # regular rotation
    if step == 1:
        # the player doesn't have fit card
        if current_card == 'none':
            if current_player == len(players) - 1:
                return True, 0, 1, players_cards, cards_deck, used_card, color
            else:
                return True, current_player + step, 1, players_cards, cards_deck, used_card, color

        # stop card case
        if current_step == STEP_SKIP_NEXT:
            if current_player + current_step == len(players):
                return True, 0, 1, players_cards, cards_deck, used_card, color
            elif current_player + current_step > len(players):
                return True, 1, 1, players_cards, cards_deck, used_card, color
            else:
                return True, current_player + current_step, 1, players_cards, cards_deck, used_card, color

        # change direction card case
        elif current_step == STEP_MOVE_BACKWARD:
            if current_player == 0:
                return True, -1, -1, players_cards, cards_deck, used_card, color
            else:
                return True, current_player + current_step, -1, players_cards, cards_deck, used_card, color

        else:  # current_step == 1 == STEP_MOVE_FORWARD
            if current_player == len(players) - 1:
                return True, 0, 1, players_cards, cards_deck, used_card, color
            else:
                return True, current_player + current_step, 1, players_cards, cards_deck, used_card, color

    # opposite rotation step=-1
    else:
        if current_card == 'none':
            if current_player == STEP_STAY_CURRENT_PLAYER:
                return True, len(players) - 1, -1, players_cards, cards_deck, used_card, color
            else:
                return True, current_player + step, -1, players_cards, cards_deck, used_card, color
        # stop card case
        if current_step == STEP_SKIP_NEXT:
            if current_player == 0:
                return True, -2, -1, players_cards, cards_deck, used_card, color
            elif current_player == 1:
                return True, -1, -1, players_cards, cards_deck, used_card, color
            else:
                return True, current_player - current_step, -1, players_cards, cards_deck, used_card, color
        # change direction card case
        elif current_step == STEP_MOVE_BACKWARD:
            if current_player == len(players) - 1:
                return True, 0, -1, players_cards, cards_deck, used_card, color
            else:
                return True, current_player - current_step, 1, players_cards, cards_deck, used_card, color

        else:  # current_step == 1 == STEP_MOVE_FORWARD
            if current_player == 0:
                return True, len(players) - current_step, -1, players_cards, cards_deck, used_card, color
            else:
                return True, current_player - current_step, -1, players_cards, cards_deck, used_card, color


if __name__ == "__main__":
    players, number_of_players = sets_players()
    cards_deck = generate_cards_deck()
    cards_deck, players_cards = game_boot(cards_deck, number_of_players)

    print('lets start to play!')
    current_card = cards_deck[0]
    while current_card[0].isalpha():
        del cards_deck[0]
        cards_deck.append(current_card)
        current_card = cards_deck[0]
    del cards_deck[0]
    used_card = [current_card]
    print('The opening card is ' + current_card)

    current_player = 0
    step = 1
    flag = True
    color = current_card[-1]
    while flag:
        flag, current_player, step, players_cards, cards_deck, used_card, color = play(players, current_player, step,
                                                                                       players_cards, cards_deck,
                                                                                       used_card, color)

    print('The winner is ' + players[current_player] + '!!!')
