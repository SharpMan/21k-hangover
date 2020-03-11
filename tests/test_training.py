import sys
sys.path.append('../')

import blackjack as BJ
import qlearning as QL

MAX_EPISODE = 5

def test_train_ql():
    for i in range(1, MAX_EPISODE):
        game = BJ.BlackJack()
        learning_agent = QL.QLearning()
        status = game.deal()

        if(status is not BJ.Status.BLACKJACK): #Game is done since distrubution and this not useful for training
            continue

        # Agent turn
        while(game.round is None):
            action = learning_agent.get_action(game.get_state())
            if(action == BJ.Action.HIT):
                game.hit()
            else:
                game.stay()

        

