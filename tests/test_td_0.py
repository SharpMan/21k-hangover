import sys
import csv

sys.path.append('../')

import td_learning as QL
import blackjack as BJ

MAX_TRAIN_EPISODE = 2500000
MAX_RUNIN_EPISODE = 1000000

def test_train_td():
    agent = QL.TDLearning()
    agent.train(MAX_TRAIN_EPISODE)
    report(agent.play_exp(MAX_RUNIN_EPISODE))
    print_state_table(agent)

def report(score):
    print("final result " + str(score))
    tot = sum(score)
    print("Win " + str(score[0] / tot * 100) + "%")
    print("Tie " + str(score[1] / tot * 100) + "%")
    print("Loose " + str(score[2] / tot * 100) + "%")

def print_state_table(learning_table):
    f = open('td_table.csv', 'w', newline='')
    with open('td_table.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["State", "Score"])
        for key, value in learning_table._value_function.items():
            hit_score = 0
            stand_score = 0


            writer.writerow([key, value])

test_train_td()

