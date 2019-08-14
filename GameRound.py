from Player import Player, PlayerNode

class LiarsDice:
    def __init__(self, start: PlayerNode, size: int) -> None:
        self.current_turn = start
        self.table_size = size


        curr = self.current_turn
        curr.player.last_bet = None
        curr.player.make_hand()
        curr = curr.next
        while curr != self.head.last:
            curr.player.last_bet = None
            curr.player.make_hand()
            curr = curr.next()

    def can_move(self, bet, player):
        if self.current_turn.last.last_bet:
            return bet[0] in range(7) and bet[1] in range(size + 1)
        else:
            if self.current_turn.last.last_bet[0] <= bet[0]:
                return bet[1] in range(self.current_turn.last.last_bet[1] + 1, size + 1)
            else:
                return bet[1] in range(self.current_turn.last.last_bet[1], size + 1)

    def move(self, dice, count):
        if (dice, count) == (0, 0):
            loser = self.call_bet(dice, count, self.current_turn)
            loser.player.size -= 1
            return LiarsDice(loser, self.table_size - 1)
        else:
            self.current_turn.last_bet = (dice, count)
            self.current_turn = self.current_turn.next
            
    def call_bet(self, dice: int, count: int, calling_player: PlayerNode):
        curr = calling_player
        total = curr.player.hand[dice]
        curr = curr.next
        while curr != calling player and total < count:
            total += curr.player.hand[dice]
        if total < count:
            return calling_player.last
        return calling_player


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf
    
    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        self.state_transf(s)

