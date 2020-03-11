import sys
sys.path.append('../')

import blackjack as BJ

def test_deal():
  game = BJ.BlackJack()

  # Test for natural blackjack
  game.deck = ['2', 'Q', '1', 'A']
  assert(game.deal() == BJ.Status.BLACKJACK)

  #Player has 21 total, True for UsableAce and Dealer has an '1' faced-up
  assert(game.get_state() == (21, True, '1'))

  # Test for good hand
  game.deck = ['3', '1', 'Q', '2']
  assert(game.deal() == BJ.Status.GOOD)
  print(game.get_state())
  assert (game.get_state() == (3, False, 'Q'))


def test_hit():
  game = BJ.BlackJack()

  # Test for STAND on 21
  game.deck = ['1', '4', '2', '5', '1', 'A']
  game.deal()
  assert(max(game.get_hand()) == 16)
  assert(game.hit() == BJ.Status.GOOD)
  assert(max(game.get_hand()) == 20)
  assert(game.hit() == BJ.Status.STAND)
  assert(max(game.get_hand()) == 21)

  # Test when player can't hit on STAND
  assert(game.hit() == BJ.Status.STAND)
  assert(max(game.get_hand()) == 21)

  # Test for BUST
  game.deck = ['7', '3', '9', '2', '5', '1', 'A']
  game.deal()
  assert(max(game.get_hand()) == 16)
  assert(game.hit() == BJ.Status.GOOD)
  assert(max(game.get_hand()) == 15)
  assert(game.hit() == BJ.Status.GOOD)
  assert(max(game.get_hand()) == 18)
  assert(game.hit() == BJ.Status.BUST)
  assert(max(game.get_hand()) == 25)
  
  # Test when player can't hit on BUST
  assert(game.hit() == BJ.Status.BUST)
  assert(max(game.get_hand()) == 25)


def test_count_hand():
  game = BJ.BlackJack()

  # Test normal hand
  hand = ['5', '1']
  hand_sum = game.count_hand(hand)
  assert(len(hand_sum) == 1)
  assert(hand_sum[0] == 6)

  # Test ace hand
  hand = ['A', 'A']
  hand_sum = game.count_hand(hand)
  assert(len(hand_sum) == 2)
  assert(hand_sum[0] == 2)
  assert(hand_sum[1] == 12)

  # Test natural blackjack
  hand = ['Q', 'A']
  hand_sum = game.count_hand(hand)
  assert(len(hand_sum) == 2)
  assert(hand_sum[0] == 11)
  assert(hand_sum[1] == 21)
  
  # Test all cards hand
  hand = [
          '1', '2', '3', '4', '5', 
          '6', '7', '8', '9', '10',
          'J', 'Q', 'K', 'A' 
         ]
  hand_sum = game.count_hand(hand)
  assert(len(hand_sum) == 1)
  assert(hand_sum[0] == 86)


def test_dealer_reveal():
  game = BJ.BlackJack()
  
  # Test LOSE on BUST
  game.status = BJ.Status.BUST
  game._dealer_reveal()
  assert(game.round == BJ.Round.LOSE)

  # Test LOSE
  game.player_hand = ['10', '8']
  game.dealer_hand = ['Q', 'K']
  game.status = BJ.Status.STAND
  game._dealer_reveal()
  assert(game.round == BJ.Round.LOSE)

  # Test WIN
  game.player_hand = ['10', '8']
  game.dealer_hand = ['10', '7']
  game.deck = ['J']
  game.status = BJ.Status.STAND
  game._dealer_reveal()
  assert(game.round == BJ.Round.WIN)
  
  # Test TIE
  game.player_hand = ['10', '8']
  game.dealer_hand = ['J', '8']
  game.status = BJ.Status.STAND
  game._dealer_reveal()
  assert(game.round == BJ.Round.TIE)

  # Test WIN on player natural blackjack
  game.player_hand = ['A', 'Q'] 
  game.dealer_hand = ['5', 'J']
  game.status = BJ.Status.BLACKJACK
  game._dealer_reveal()
  assert(game.round == BJ.Round.WIN)

  # Test LOSE on dealer natural blackjack
  game.player_hand = ['5', '6', 'J'] 
  game.dealer_hand = ['K', 'A']
  game.status = BJ.Status.STAND
  game._dealer_reveal()
  assert(game.round == BJ.Round.LOSE)

  # Test TIE on both natural blackjack
  game.player_hand = ['A', 'Q']
  game.dealer_hand = ['K', 'A']
  game.status = BJ.Status.BLACKJACK
  game._dealer_reveal()
  assert(game.round == BJ.Round.TIE)


test_deal()
test_hit()
test_count_hand()
test_dealer_reveal()
