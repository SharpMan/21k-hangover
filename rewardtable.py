from blackjack import Action
from blackjack import Round

PLAYER_COUNT = list(range(2, 22))
#DEALER_COUNT = ['1','2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
DEALER_COUNT = list(range(2,12))
USABLE_ACE = [True, False]
#SOFT_HAND = [True, False]


class QRewardTable:
    def __init__(self):
        states = []
        for player_count in PLAYER_COUNT:
            for usable_ace in USABLE_ACE:
                for dealer_count in DEALER_COUNT:
                    states.append((player_count, usable_ace, dealer_count))
        #list comprehension below constructs a "states" length list of lists of the form [0,0] 
        self.table = dict(zip(states, [ dict({Action.HIT: 0, Action.STAY: 0}) for _ in range(len(states))]))
        self.table[Round.LOSE] = dict({Action.HIT: -1, Action.STAY: -1})
        self.table[Round.TIE] = dict({Action.HIT: 0, Action.STAY: 0})
        self.table[Round.WIN]  = dict({Action.HIT: 1.5, Action.STAY: 1.5})


class TDRewardTable:
    def __init__(self):
        states = []
        for player_count in PLAYER_COUNT:
            for usable_ace in USABLE_ACE:       
                for dealer_count in DEALER_COUNT:
                    states.append((player_count, usable_ace, dealer_count))
        #list comprehension below constructs a states length list of 0's
        self.table = dict(zip(states, [ 0 for _ in range(len(states))]))
        self.table[Round.LOSE] = -1
        self.table[Round.TIE] = 0
        self.table[Round.WIN]  = 1

