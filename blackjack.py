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
  '1': [1],
  '2': [2],
  '3': [3],
  '4': [4],
  '5': [5],
  '6': [6],
  '7': [7],
  '8': [8],
  '9': [9],
  '10':[10],
  'J': [10],
  'Q': [10],
  'K': [10],
  'A': [1, 11],
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

    if(is_ace and sum_of_other <= 21): return [sum_of_hand, sum_of_other]
    else: return [sum_of_hand]


  def get_hand(self) -> list:
    return self.count_hand(self.player_hand)


  def hit(self) -> bool:
    if(len(self.deck) <= 0): self.deck = self.new_deck()
  
    self.player_hand.append(self.deck.pop())



game = BlackJack()
print(game.deck)
game.deal()
print(game.player_hand)
print(game.dealer_hand)

hand_sum = game.get_hand()
if(len(hand_sum) == 2):
  print(hand_sum[0], hand_sum[1])
else:
  print(hand_sum[0])


