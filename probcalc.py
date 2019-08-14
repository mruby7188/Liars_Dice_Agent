"""probability_caluclator.py

This file predicts the probability distribution for a given hand of
'Liars Dice'.  The class is intended to be used in conjuntion with
the 'Liars Dice' game to inform players moves and to help computer
players to make moves.
"""

# TODO
# -- Represent with a Markov Chain, where Z_i == 1 w.p. (1/6 or 1/3)
#       and Z_i == -1 w.p. (5/6 2/3).

import numpy as np
from scipy.stats import binom
from typing import List, Tuple, T, Dict, Union

ROUND_MOVES = 0


class probcalc:
    """
    Calculates the conditional distribution of hands given your hand.

    Attributes:
        dist: np.matrix(float[][]): The probability, p, of a dice face i
                                    having at-least j occurances w where
                                    probs[i][j] = p.
        __hand (Dict[int, int]): The counts of each dice in the players
                                hand, so that my_hand[i] returns the
                                number of dice with face i.
        size (int): Number of dice in play.
        wild (bool): Whether or not 1's are wild.
        hand_size (int): Number of dice in my hand
    """

    def __init__(self,
                 hand_size: int,
                 my_hand: Dict[int, int],
                 total_dice: int,
                 isWild: bool) -> None:

        self.__hand = my_hand
        self.hand_size = hand_size
        self.size = total_dice
        self.wild = isWild
        self.dist = self.__calculate_distribution()

    def __copy__(self: T) -> T:
        return probcalc(self.size, self.__hand, self.size, self.wild)

    def __eq__(self: T, s2: T) -> bool:
        return ((self.wild == s2.wild) and (self.__hand == s2.hand) and
                (self.dist == s2.probs) and (self.size == s2.size))

    def __calculate_distribution(self) -> List[List[float]]:
        """
        Populates the probability distribution of the round, if it has
        not been calculated yet.

        Letting X_i = a + (#{Z_i = dice} : i in [0, i]) where
            a = self.__hand[dice], we can represent this as a Markov
            chain, where:

        P(X_i = k - a) =
            P { SUM_{k-a}^{size - len(self.__hand)}
                [X_i] >= n - k - a }

         = Choose(size-len(self.__hand), size-a)

        Returns:
            A 7 x (self.total + 1) dimensional np.matrix where A[i][j]
            is the probability that there are at-least j of that dice i
            in the field.
        """
        if not self.wild:
            p = 1 / 6
            probs = [[0] * (self.size + 1)]
        else:
            p = 1 / 3
            probs = [[0] * (self.size + 1)] * 2

        n = (self.size - self.hand_size)

        x = np.arange(0, n + 1)

        dist = list(1 - binom.cdf(x - 1, n, p))

        for i in range(1, 7):
            cdf = [1.0] * self.__hand[i]
            cdf += dist
            cdf += [0.0] * (self.__hand[i] + n)
            probs.append(cdf)

        return np.matrix(probs)

    def opponent_probability(self,
                             opponent_size: int,
                             play: Tuple[int, int]) -> float:
        """
        Uses your hand size and the opponents hand size to estimate the
        likelyhood that your opponent is not lying, or will not catch
        you lying.
        """
        unknown = play[2] - self.__hand[play[1]]
        if unknown <= 0:    # must be at least the claimed number in play.
            return 1.0
        elif self.dist[play] == 0.0:
            return 0.0
        if self.wild:
            p = 1 / 3
        else:
            p = 1 / 6

        """
        Calculate probability that the player has n dice in their hand and
        that they are right.
        """
        dice_remain = self.size - self.hand_size - opponent_size

        """
        Probability that at least the wagered number of dice remain given
        they have k dice, and the number in your hand.

        P(S_n >= m | X_(opponent)) = 
            [P(S_{n - 1} >= m - k) * P(X_1 = k)]  
            -------------------------------------
                         P(S_n >= m)
        """
        probs = [((1 - binom.cdf(unknown - k - 1, dice_remain, p)) *
                  (binom.pmf(k, opponent_size, p))) /
                 self.dist[play] for k in range(opponent_size)]
