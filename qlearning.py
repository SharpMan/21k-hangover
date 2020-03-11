import numpy as np

from blackjack import Action


class QLearning():

    def __init__(self):
        self.Q = {}
        self._learning_rate = .7  # gamma
        self._discount = .9       # tetha
        self._epsilon = 0.2

    def get_action(self, current_state):
        if (current_state in self.Q and np.random.uniform(0, 1) < self._epsilon):
            action = max(self.Q[current_state], key=self.Q[current_state].get)
        else:
            action = np.random.choice([Action.HIT, Action.STAY])
            if current_state not in self._Q:
                self._Q[current_state] = {}
            self._Q[current_state][action] = 0

        return action

    def update_table(self, old_state, action, new_state, reward):
        cur_reward = self._Q[old_state][action]

        bonus = 0
        if new_state in self._Q:
            bonus = self._discount * self._Q[new_state][max(self._Q[new_state], key=self._Q[new_state].get)]

        self._Q[old_state][action] = (1- self._learning_rate) * cur_reward + self._learning_rate*(reward+ bonus)

