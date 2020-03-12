from blackjack import Action

PLAYER_COUNT = list(range(2, 22))
DEALER_COUNT = list(range(1,12))
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
        self.table = dict(zip(states, [ [0]*2 for _ in range(len(states))]))


class TDRewardTable:
    def __init__(self):
        states = []
        for player_count in PLAYER_COUNT:
            for usable_ace in USABLE_ACE:       
                for dealer_count in DEALER_COUNT:
                    states.append((player_count, usable_ace, dealer_count))
        #list comprehension below constructs a states length list of 0's
        self.table = dict(zip(states, [ 0 for _ in range(len(states))]))


