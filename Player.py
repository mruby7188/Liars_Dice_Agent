"""Player.py

This file creates a Player class that plays a game of Liars Dice.
"""

# TODO
# -- Use probability calculations to estimate each players hand,
#       as number of samples grows larger, use predictions with
#       higher certainty.
# -- Possibly weight predictions by the number of times the player
#       uses that number.
# -- Consider decreasing weight when player follows the prior bet
#       if they had not bet that number before.
# -- Possibly Gradient Descent, using each round as an episode.

from math import log, sqrt
from random import randint, uniform, choice
from typing import Dict, List, Optional, T, Tuple
from scipy.stats import norm

import numpy as np

from probcalc import probcalc


class Player:
    """
    Attributes:

        craziness (float [0, 0.3]): The probability with which the
                                  player acts randomly.
        aggressiveness (float [0, 0.4]): Probability threshold that the
                                         player accuses player of
                                         bluffing.
        size (int <= 5): The number of dice the player has.
        total_dice (int): The total dice in play.
        name (str): The players name.
        probs (probcalc): The probability distribution for this round
        opponents_hands List[int]: Size of opponents hands, index 0
                                   refers to the next players hand and
                                   index n_players - 1 is the prior
                                   players hand.
    """

    def __init__(self,
                 size: int,
                 total_dice: int,
                 opponents: List[int],
                 name: str = None) -> None:

        self.size = size
        self.__aggressiveness = uniform(0, 0.4)
        self.__craziness = uniform(0, 0.3)
        self.name = name
        self.total = total_dice
        self.opponent_hands = opponents
        self.__probs = None
        self.wild = False
        self.hand = None

    def set_wild(self, isWild: bool) -> None:
        self.__probs = probcalc(self.hand, self.total, self.total, self.wild)

    def get_count(self, dice: int) -> int:
        n = self.hand[dice]
        if self.wild:
            return n + self.hand[1]
        else:
            return n

    def __hash__(self):
        return self.name.__hash__()

    def greet(self) -> str:
        if self.__craziness > 0.2:
            if self.__aggressiveness > 0.3:
                p1 = "I'm a WILDCARD!!"
            else:
                p1 = "you better watch your step around me."
        elif self.__craziness < 0.05:
            if self.__aggressiveness < 0.2:
                p1 = "I've got my eye on you..."
            else:
                p1 = "I play by dice close to my chest."
        else:
            p1 = "I will be keeping you on your toes."
        return "Hi, my name is %s and %s" % (self.name, p1)

    def __str__(self) -> str:
        return "%s has %d dice remaining." % (self.name, self.size)

    def __eq__(self: T, s2: T) -> bool:
        return self.name == s2.name and self.hand == s2.hand

    def take_turn(self, last=None) -> Tuple[int, int]:
        """
        Makes a move based on the best probability of either
        successfully calling a bluff, or not having a bluff called.

        Returns:
            Tuple[int, int]: Containing the dice and amount.  Returns
                             (0, 0) if calling a bluff.
        """
        crazy = (uniform(0, 1) < self.__craziness)
        ones = self.hand[1]
        d = np.argmax(list(self.hand.values())[2:])
        if len(self.opponent_hands) == 1 and self.opponent_hands[0] == 1:
            if self.size == 1:
                return one_on_one(last, self.hand[d])

        if not last:
            if len(self.opponent_hands) == 1 and sum(self.hand.values()) == 1:
                return (d, self.hand[d])
            if crazy:
                d = choice(range(1, 7))
                count = choice(range(1, (self.size // 4) + 1))
                return (d, count)
            if ones >= self.hand[d]:
                return (1, ones)
            return (d, ones + self.hand[d])

        k = last[1] - self.hand[last[0]]
        play = (self.__probs[last[0], k] < self.__aggressiveness)

        if (play and not crazy) or (not play and crazy):
            return (0, 0)
        play = self.__play(last)

        if self.__probs[last] - self.__probs[play[0], play[1] - ones] > 0.15:
            return (0, 0)

        if should_call(play, self.hand, self.total, self.wild):
            return (0, 0)

        return play

    def __play(self, last: Tuple[int, int]) -> Tuple[int, int]:
        """
        Makes a move for the player.
        """
        if not self.wild or not last:
            k = self.hand[1]
        else:
            k = 0

        count = last[1] - k
        low = list(self.__probs[:last[0] + 1, count + 1].T)
        high = list(self.__probs[last[0] + 1:, count].T)
        moves = np.array(low + high)
        d = np.argmax(list(moves))
        return (d, k + self.hand[d])

    def start_new_round(self, lost, new_hand) -> None:
        """
        Prepares the player for a new round and removes a dice if they
        lost in the last round.
        """
        self.hand = new_hand
        self.size = len(new_hand) - 1
        self.wild = False
        self.__probs = None

    def make_hand(self) -> Dict[int, int]:
        """
        Randomly creates a new hand for the player.
        """
        hand = {n: 0 for n in range(7)}
        for _ in range(self.size):
            hand[randint(1, 6)] += 1
        self.hand = hand


def should_call(last, my_hand, total_dice, wild) -> bool:
    """
    Returns False if the probability of the last play is greater than
    the minimum of the confidence interval. returns True otherwise.
    """
    if wild:
        p = 1 / 3
    else:
        p = 1 / 6
    n_s = last[1] - my_hand[last[0]]
    if wild:
        n_s -= my_hand[1]
    if n_s >= 0:
        return False

    n_f = total_dice - my_hand - n_s
    p_hat = get_CI(n_s, n_f)

    if p_hat < p:
        return False
    return True


def get_CI(n_s: int, n_f: int) -> float:
    """
    Calculates the Binomial proportion confidence interval using the
    Wilson score interval (found here: https://en.wikipedia.org/wiki/
    Binomial_proportion_confidence_interval#Wilson_score_interval).

    Returns:
        Low end of 90% C.I. for event probability.
        (i.e. 10% likelyhood that the events probability is not higher
         than the value.)
    """
    z = norm.ppf(0.8)   # 90% confidence interval
    a = (n_s + z ** 2 / 2) / (n_s + n_f + z ** 2)
    b = z / ((n_s + n_f) + z ** 2) * \
        sqrt((n_s * n_f / (n_s + n_f)) + z ** 2 / 4)
    return a - b


def one_on_one(last: int, my_dice: Dict[int, int]) -> int:
    """
    If both players have one dice remaining bet on the sum of both hands.
    """
    mine = max(my_dice.values())
    bet = mine + randint(1, 6)
    if last:
        if last <= mine:
            return mine + 1
        elif last <= mine + 2:
            return mine + (last - mine) + 1
        while last == bet:
            bet = mine + randint(1, 6)
        return bet
    return bet


# def end_game(opponenent_size: int,
#              my_hand: Dict[int, int],
#              last_play: Tuple[int, int],
#              wild: bool) -> Tuple[int, int]):

#     face = last_play[0]
#     count = last_play[1]

#     d = np.argmax(list(self.hand.values())[2:])
#     my_size = sum(my_hand.values())
#     if wild:
#         unknown = count - (my_hand[face] - ones)
#     else:
#         unknown = count - my_hand[d]

#     if unknown > opponenent_size):
#         return (0, 0)

#     if my_hand[d] > count or (d > face and my_hand[d] == count):
#         return (d, my_hand[d])

#     return (0, 0)

class PlayerNode:
    def __init__(self, player: Player, size: int, last=None):
        self.player = player
        self.last = last
        self.next = None
        self.last_bet = None
