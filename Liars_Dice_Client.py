#! python3
"""
Liars_Dice_Client.py

Runs a game of Liar's Dice where the user can choose the number of
computer players, up to 12 total players.

Rules for the game can be found at:
https://www.wikihow.com/Play-Liar%27s-Dice

This game uses the variation that on when the game is down to two
players and each player has one dice remaining; each player bets on the
sum of the two dice and the closest player wins.

Uses name file from
'https://github.com/hadley/data-baby-names/blob/master/baby-names.csv'
"""
import os
import sys
import tkinter
import pandas as pd
from random import uniform, choice, randint
from scipy.stats import binom
from Player import Player, PlayerNode
from typing import Dict, List, Optional, T, Tuple

NAMES = pd.read_csv('us-names.csv')
TOTAL_DICE = 0
HAND_SIZES = []
LOST = {}
MOVES = {}
NAMES = []
ROUND = 0
TABLE_SIZE = 0
PLAYER_HANDS = {n: 0 for n in range(1, 7)}
USER_HAND = {n: 0 for n in range(1, 7)}


def setup():
    print("Welcome to Liars Dice!")
    if len(sys.argv) == 2:
        PLAYERS.append(sys.argv[1])
    else:
        name = input("what is your players name? ")
        front = PlayerNode(name, 5)
        curr = front
        NAMES.append(name)
    for _ in range(5):
        d = randint(1, 6)
        USER_HAND[d] += 1
        PLAYER_HANDS[d] += 1
    while True:
        try:
            TABLE_SIZE = int(input("How many other players are there? "))
        except ValueError:
            TABLE_SIZE = print("Please enter a valid integer in [1, 11] ")
            continue
        else:
            if TABLE_SIZE > 11:
                TABLE_SIZE = print("Please enter a valid integer in [1, 11] ")
                continue
            break
    TABLE_SIZE += 1
    HAND_SIZES = [5] * TABLE_SIZE 
    TOTAL_DICE = 5 * TABLE_SIZE
    for _ in TABLE_SIZE:
        while name in NAMES:
            name = choice(NAMES.name[NAMES.percent <= uniform(0, 1)])
        NAMES.append(name)
        p = Player(5, TOTAL_DICE, HAND_SIZES, name)
        curr.next = PlayerNode(p, 5, curr)
        curr = curr.next
    front.last = curr
 
    # Randomly Choose the first player.
    firstPlayer = choice(NAMES)

    # Make front the first player
    while curr.player.name != firstPlayer:
        curr = curr.next

    self.PLAYERS = curr

    print("Starting Game.")
    runGame()


def runGame():
    print("Game Running")

    while TABLE_SIZE > 1:
        if TABLE_SIZE == 2 and HAND_SIZES[np.argmax(HAND_SIZES)] == 1:
            loser = endGame()
        else:
            loser = runRound(first_player)
            HAND_SIZES[loser] -= 1
            for p in PLAYERS:
                if isinstance(p, Player):
                    p.make_hand
                    for d, count in p.hand.values():
                        PLAYER_HANDS[d] += count
                else:
                    for _ in range(5):
                        d = randint(1, 6)
                        USER_HAND[d] += 1
                        PLAYER_HANDS[d] += 1


# def startGame(players: List[int]) -> int:
#     print("Game Started")
#     max_sum = 0
#     for n in players:
#         s = randint(1, 6) + randint(1, 6)
#         if s > max_sum:
#             max_sum = s
#             max_ind = [n]
#         elif s == max_sum:
#             max_ind.append(n)
#     if len(max_ind) > 1:
#         return startGame(max_ind)
#     return max_ind[0]


def endGame():
    """
    When each player has only one dice left they will each guess the 
    sum of the dice, with the loser from the last round goind first.

    The closest to the actual sum wins the game.
    """
    print("Beginning Sudden Death, Player who guesses closest to the" +
          " total of the two dice is the winner.")
    guesses = {}
    hands = []
    for p in PLAYERS:
        p.hand = randint(1, 6)
        hands.append[randint(1, 6)]
        while True:
            if isinstance(p, Player):
                guess[p.name] = p.take_turn
                break
            else:
                try:
                    guess = int(input("Please guess the sum " +
                                      "for the two dice."))
                    continue
                except ValueError:
                    print("Value must be a single integer.")
                    continue
                else:
                    if guess <= 1:
                        print("You must guess at least 2.")
                        continue
                    
                    break
    actual = sum(hands)
    diff1 = abs(guess[Players[0]] - actual)
    if diff1 <
    


def runRound(ind: int) -> int:
    print("Running Round")
    p = PLAYERS[ind]
    last = None
    while True:
        if isinstance(p, Player):
            next = p.take_turn(last)
        else:
            next = get_input(last)
        if next != (0, 0):
            if p.name in MOVES.keys():
                MOVES[p.name].append(next)
            else:
                MOVES[p.name] = [next]
            n = (n + 1) % TABLE_SIZE
            p = PLAYERS[ind]
            last = next
            continue
        else:
            break

    if PLAYER_HANDS[last[0]] < last[1]:
        return n - 1
    else:
        return n


def get_input(last=None) -> Tuple[int, int]:
    face = False
    while True:
        try:
            if not face:
                face = int(
                    input("Please choose a dice to bet or 0 to call.\n")
                    .strip())
            else:
                count = int(input("Please make a wager.\n").strip())
        except ValueError:
            print("Please enter a valid integer.")
            continue
        else:
            if not face:
                if face in range(1, 7):
                    face = True
                    continue
                elif face == 0 and last:
                    return 0, 0
                else:
                    print("Integer must be greater than 1 and " +
                          "less than 6.")
                    continue
            elif count <= 0 or last:
                if not last:
                    print("Wager must be greater than 0.")
                    continue
            elif count < last[1]:
                print("Wager must be at least equal to the last bet.")
                continue
            elif face <= last[0] and count == last[1]:
                print("To bet a face smaller or equal to the last " +
                      "wager, it must bet a higher amount.")
                face = check_change_face()
                continue
            else:
                break

    return face, count


def check_change_face() -> bool:
    face = True
    while True:
        try:
            change = str(input("Would you like to choose a new face?")
                         .strip('.'))
        except ValueError:
            print("Please enter y/n")
        else:
            if change.lower() in ['y', 'yes']:
                face = False
            elif change.lower() not in ['n', 'no']:
                print("Please enter y/n")
                continue
            break
    return face


def getFaceCounts() -> Dict[int, int]:
    faces = {n: 0 for n in range(1, 7)}
    for f, c in (PLAYER_HANDS.values() + USER_HAND.values):
        faces[f] += c
    return faces


if __name__ == "__main__":
    setup()
