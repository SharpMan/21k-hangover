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
    self.num_of_players = 2
    self.player_hand = []
    self.dealer_hand = []
    self.dealt = False

  def new_deck(self) -> list:
    deck = DECK_OF_CARDS.copy()
    new_deck = []   

    while (len(deck) > 0):
      new_deck.append(deck.pop(random.randint(0,len(deck)-1)))

    return new_deck

  def deal(self) -> bool:
    if(self.dealt): return False
    
    cards_dealt = 0
    player_turn = 0
    while(cards_dealt < 2*self.num_of_players ): 
      if(len(self.deck) <= 0): self.deck = self.new_deck()
      
      # deal to player
      if(player_turn < self.num_of_players-1): 
        self.player_hand.append(self.deck.pop())
        player_turn += 1
      # deal to a dealer
      else:
        self.dealer_hand.append(self.deck.pop())
        player_turn = 0

      cards_dealt += 1

    self.dealt = True
    return True

game = BlackJack()
print(game.deck)
game.deal()
print(game.player_hand)
print(game.dealer_hand)
