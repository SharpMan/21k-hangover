import random

DECK_OF_CARDS = [
  '1', '1', '1', '1',
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
  '1': (1),
  '2': (2),
  '3': (3),
  '4': (4),
  '5': (5),
  '6': (6),
  '7': (7),
  '8': (8),
  '9': (9),
  '10': (10),
  'J': (10),
  'Q': (10),
  'K': (10),
  'A': (1, 11),
}

class BlackJack():
  
  def __init__(self):
    self.deck = self.new_deck()
    self.player_hand = []
    self.dealer_hand = []

  def new_deck(self) -> list:
    deck = DECK_OF_CARDS.copy()
    new_deck = []   

    while (len(deck) > 0):
      new_deck.append(deck.pop(random.randint(0,len(deck)-1)))

    return new_deck

game = BlackJack()
print(game.deck)
