import numpy as np

from blackjack import Action, BlackJack, Round, Status
from rewardtable import QRewardTable


class QLearning():

    def __init__(self):
        self.Q = QRewardTable()
        self._alpha = .1           #learning rate
        self._gamma = .9         #discount factor
        self._epsilon = .3       #exploration probability

    def get_action(self, current_state):
        if (current_state in self.Q.table and np.random.uniform(0, 1) < self._epsilon):
            action = max(self.Q.table[current_state], key=self.Q.table[current_state].get)
        else:
            action = np.random.choice([Action.HIT, Action.STAY])
            #if current_state not in self.Q.table: self.Q.table[current_state] = {}
            #self.Q.table[current_state][action] = 0
        return action

    def learn(self, old_state, action, new_state, reward):
        cur_reward = self.Q.table[old_state][action]
        bonus = 0
        #if new_state in self.Q.table:
        max_arg = max(self.Q.table[new_state], key=self.Q.table[new_state].get)
        if old_state == new_state:
            bonus = 0.0
        else:
            bonus = self._gamma * self.Q.table[new_state][max_arg]
        self.Q.table[old_state][action] = cur_reward + (self._alpha * (reward + bonus - cur_reward))

    def train(self, episodes):
        game = BlackJack()
        win  = 0
        tie  = 0
        lose = 0
        old_epsilon = self._epsilon
        #self._epsilon = 0.0
        
        for episode in range(1,episodes+1):
            if self._epsilon < old_epsilon:
                self._epsilon -= self._epsilon * (episode / episodes)
            else:
                self._epsilon == old_epsilon

            status = game.deal()
            if(status is Status.BLACKJACK):
                win += 1
                continue
            # Agent turn
            while game.round is None:
                cur_state = game.get_state()
                action = self.get_action(cur_state)
                
                if(action == Action.HIT):
                    game.hit()
                else:
                    game.stay()
                
                if game.round is None:
                    new_state = game.get_state()
                    self.learn(cur_state, action, new_state, 0)
                else:
                    reward_state = game.round
                    self.learn(cur_state, action, cur_state, self.Q.table[reward_state][action])

            if game.round == Round.WIN:
                win += 1
            elif game.round  == Round.TIE:
                tie += 1
            else:
                lose += 1
        self._epsilon = old_epsilon
        return (win, tie, lose)

            
    def play(self, episodes):
        game = BlackJack()
        win  = 0
        tie  = 0
        lose = 0
        old_epsilon = self._epsilon
        self._epsilon = 1.0
            
        for i in range(episodes):
            status = game.deal()
            if(status is Status.BLACKJACK):
                win += 1
                continue
            # Agent turn
            while game.round is None:
                cur_state = game.get_state()
                action = self.get_action(cur_state)
                
                if(action == Action.HIT):
                    game.hit()
                else:
                    game.stay()

            if game.round == Round.WIN:
                win += 1
            elif game.round  == Round.TIE:
                tie += 1
            else:
                lose += 1
        self._epsilon = old_epsilon
        return (win, tie, lose)
