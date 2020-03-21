import random
from enum import Enum

DECK_OF_CARDS = [
    '2', '2', '2', '2',
    '3', '3', '3', '3',
    '4', '4', '4', '4',
    '5', '5', '5', '5',
    '6', '6', '6', '6',
    '7', '7', '7', '7',
    '8', '8', '8', '8',
    '9', '9', '9', '9',
    '10', '10', '10', '10',
    'J', 'J', 'J', 'J',
    'Q', 'Q', 'Q', 'Q',
    'K', 'K', 'K', 'K',
    'A', 'A', 'A', 'A',
]

CARD_VALUES = {
    '2': [2],
    '3': [3],
    '4': [4],
    '5': [5],
    '6': [6],
    '7': [7],
    '8': [8],
    '9': [9],
    '10': [10],
    'J': [10],
    'Q': [10],
    'K': [10],
    'A': [1, 11],
}


class Status(Enum):
    BUST = 0
    GOOD = 1
    STAND = 2
    BLACKJACK = 3


class Round(Enum):
    LOSE = 0
    WIN = 1
    TIE = 2

class Action(Enum):
    HIT = 0
    STAY = 1

class BlackJack():

    def __init__(self):
        self.deck = self.new_deck()
        self.num_of_players = 2
        self.player_hand = []
        self.dealer_hand = []
        self.round = None
        self.status = None

    def new_deck(self) -> list:
        deck = DECK_OF_CARDS.copy()
        new_deck = []

        while (len(deck) > 0):
            new_deck.append(deck.pop(random.randint(0, len(deck) - 1)))

        return new_deck

    def get_state(self):
        player_hand = self.get_hand()
        usable_ace_flag = (len(player_hand) > 1)
        return (max(player_hand), usable_ace_flag, CARD_VALUES[self.get_face()][0])

    def reset(self):
        self.player_hand = []
        self.dealer_hand = []
        self.round = None
        self.status = None

    def deal(self) -> Status:
        self.reset()

        cards_dealt = 0
        player_turn = 0
        while (cards_dealt < 2 * self.num_of_players):
            if (len(self.deck) <= 0): self.deck = self.new_deck()

            # deal to player
            if (player_turn < self.num_of_players - 1):
                self.player_hand.append(self.deck.pop())
                player_turn += 1
            # deal to a dealer
            else:
                self.dealer_hand.append(self.deck.pop())
                player_turn = 0

            cards_dealt += 1

        if (21 in self.get_hand()):
            self.status = Status.BLACKJACK
            self._dealer_reveal()
            return self.status
        else:
            self.status = Status.GOOD
            return self.status

    def count_hand(self, hand: list) -> int:
        sum_of_hand = 0
        sum_of_other = 0
        is_ace = False
        for card in hand:

            if (card == 'A' and not is_ace):
                sum_of_hand += CARD_VALUES[card][0]
                sum_of_other += CARD_VALUES[card][1]
                is_ace = True
            else:
                sum_of_hand += CARD_VALUES[card][0]
                sum_of_other += CARD_VALUES[card][0]

        if (is_ace and sum_of_other <= 21):
            return [sum_of_hand, sum_of_other]
        else:
            return [sum_of_hand]

    def get_hand(self) -> list:
        return self.count_hand(self.player_hand)

    def get_face(self) -> chr:
        if (len(self.dealer_hand) < 2): return -1
        return self.dealer_hand[0]

    def hit(self) -> Status:
        if (self.status != Status.GOOD): return self.status
        if (len(self.deck) <= 0): self.deck = self.new_deck()

        self.player_hand.append(self.deck.pop())

        if (max(self.get_hand()) == 21): #can't get more card
            self.status = Status.STAND
            self._dealer_reveal()
            return Status.STAND
        elif (max(self.get_hand()) < 21):
            return Status.GOOD
        else:
            self.status = Status.BUST
            self._dealer_reveal()
            return Status.BUST

    def stand(self) -> Status:
        if (self.status != Status.GOOD): return Status
        self.status = Status.STAND
        self._dealer_reveal()
        return self.status

    def _dealer_reveal(self):

        # Check if player busted
        if (self.status == Status.BUST):
            self.round = Round.LOSE
            return

        dealer_hand_sum = self.count_hand(self.dealer_hand)
        player_hand_sum = self.count_hand(self.player_hand)
        # Check if both player and dealer for a natural blackjack
        if (self.status == Status.BLACKJACK):
            if (21 in dealer_hand_sum):
                self.round = Round.TIE
            else:
                self.round = Round.WIN
            return
        elif (21 in dealer_hand_sum):
            self.round = Round.LOSE
            return

        dealer_best = max(dealer_hand_sum)
        player_best = max(player_hand_sum)
        while (dealer_best < player_best and dealer_best < 17):
            if (len(self.deck) <= 0): self.deck = self.new_deck()

            self.dealer_hand.append(self.deck.pop())
            dealer_best = max(self.count_hand(self.dealer_hand))

        # Check if dealer busted
        if (dealer_best > 21):
            self.round = Round.WIN
            return
        # Check both hands
        if(player_best > dealer_best):
            self.round = Round.WIN
        elif (dealer_best == player_best):
            self.round = Round.TIE
        else:
            self.round = Round.LOSE
        return
