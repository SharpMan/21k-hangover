import numpy as np
from collections import defaultdict
import random

from blackjack import Action
import blackjack as BJ

class TDLearning():

    def __init__(self):
        self._value_function = defaultdict(float)
        self._counter_state = defaultdict(int)
        self._counter_state_action = defaultdict(int)
        self._alpha = .1  # learning rate
        self._gamma = .9  # discount factor
        self._lambda = 0.9
        self._n_zero = 100 # epislon greedy constant

    def get_action(self, epsilon, current_state, is_training=True):
        if not is_training or (current_state in self._value_function and random.random() < epsilon):
            if self._value_function[current_state, Action.STAY] > self._value_function[current_state, Action.HIT]:
                action = Action.STAY
            else:
                action = Action.HIT
        else:
            action = np.random.choice([Action.HIT, Action.STAY])
            if current_state not in self._value_function:
                self._value_function[current_state, Action.HIT] = 0
                self._value_function[current_state, Action.STAY] = 0

        return action

    def train(self, EPS):
        win = 0
        tie = 0
        lose = 0
        for episode in range(EPS):
            eligibility_trace = defaultdict(float)
            game = BJ.BlackJack()
            status = game.deal()
            if status is BJ.Status.BLACKJACK:  # Game is over right after distrubution and this not useful for training
                continue
            current_state = game.get_state()
            epsilon = self._n_zero / float(self._n_zero + self._counter_state[current_state])
            current_action = self.get_action(epsilon, current_state)

            while (game.round is None):
                self._counter_state[current_state] += 1
                self._counter_state_action[(current_state, current_action)] += 1

                if (current_action == BJ.Action.HIT):
                    status = game.hit()
                    if (status is BJ.Status.GOOD):  # non-terminal state
                        continue
                else:
                    status = game.stand()
                    if (status is not BJ.Status.STAND):  # non-terminal state
                        continue

                if (game.round == BJ.Round.WIN):
                    reward = 1
                elif (game.round == BJ.Round.LOSE):
                    reward = -1
                else:
                    reward = 0

                #next action
                next_state = game.get_state()
                next_action = self.get_action(epsilon, next_state)
                delta = reward + self._gamma * self._value_function[(next_state, next_action)] - \
                        self._value_function[(current_state, current_action)]

                alpha = 1.0 / self._counter_state_action[(current_state, current_action)]
                eligibility_trace[(current_state, current_action)] += 1

                #update table
                for key in self._value_function:
                    self._value_function[key] +=  alpha * delta * eligibility_trace[key]
                    eligibility_trace[key] *= self._gamma * self._lambda

                current_state = next_state
                current_action = next_action

            if game.round == BJ.Round.WIN:
                win += 1
            elif game.round == BJ.Round.TIE:
                tie += 1
            else:
                lose += 1

        return (win, tie, lose)

    def play_exp(self, EPS):
        win = 0
        tie = 0
        lose = 0
        for episode in range(EPS):
            eligibility_trace = defaultdict(float)
            game = BJ.BlackJack()
            status = game.deal()
            if status is BJ.Status.BLACKJACK:  # Game is over right after distrubution and this not useful for training
                win += 1
                continue
            current_state = game.get_state()
            current_action = self.get_action(0, current_state, False)

            while (game.round is None):
                self._counter_state[current_state] += 1
                self._counter_state_action[(current_state, current_action)] += 1

                if (current_action == BJ.Action.HIT):
                    status = game.hit()
                    # game_history.append([previous_state, action, game.get_state(), step])
                    if (status is BJ.Status.GOOD):  # non-terminal state
                        continue
                else:
                    status = game.stand()
                    # game_history.append([previous_state, action, game.get_state(), step])
                    if (status is not BJ.Status.STAND):  # non-terminal state
                        continue

                if (game.round == BJ.Round.WIN):
                    reward = 1
                elif (game.round == BJ.Round.LOSE):
                    reward = -1
                else:
                    reward = 0

                # next action
                next_state = game.get_state()
                next_action = self.get_action(0, next_state, False)
                eligibility_trace[(current_state, current_action)] += 1

                current_state = next_state
                current_action = next_action

            if game.round == BJ.Round.WIN:
                win += 1
            elif game.round == BJ.Round.TIE:
                tie += 1
            else:
                lose += 1
        return (win, tie, lose)


    def learn(self, old_state, action, new_state, reward):
        cur_reward = self._value_function[old_state][action]
        bonus = 0

        if new_state in self._value_function:
            max_arg = max(self._value_function[new_state], key=self._value_function[new_state].get)
            bonus = self._gamma * self._value_function[new_state][max_arg]

        self._value_function[old_state][action] = cur_reward + (self._alpha * (reward + bonus - cur_reward))
