import numpy as np

from blackjack import Action


class QLearning():

    def __init__(self):
        self.Q = {}
        self._alpha = .2           #learning rate
        self._gamma = .9           #discount factor
        self._epsilon = .2         #exploration probability

    def get_action(self, current_state):
        if (current_state in self.Q and np.random.uniform(0, 1) < self._epsilon):
            action = max(self.Q[current_state], key=self.Q[current_state].get)
        else:
            action = np.random.choice([Action.HIT, Action.STAY])
            if current_state not in self._Q:
                self._Q[current_state] = {}
            self._Q[current_state][action] = 0

        return action

    def learn(self, old_state, action, new_state, reward):
        cur_reward = self._Q[old_state][action]
        bonus = 0

        if new_state in self._Q:
            max_arg = max(self._Q[new_state], key=self._Q[new_state].get)
            bonus = self._gamma * self._Q[new_state][max_arg]

        self._Q[old_state][action] = cur_reward + (self._alpha * (reward + bonus - cur_reward))

