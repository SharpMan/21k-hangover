import sys
import csv

sys.path.append('../')

import blackjack as BJ
import qlearning as QL

MAX_EPISODE = 2550000


def test_train_ql():
    learning_agent = QL.QLearning()
    for i in range(1, MAX_EPISODE):
        game = BJ.BlackJack()
        status = game.deal()
        step = 0

        if (status is BJ.Status.BLACKJACK):  # Game is over right after distrubution and this not useful for training
            continue

        game_history = []

        # Agent turn

        while (game.round is None):
            # When action  return STAND or BUST the loop should exit
            step += 1
            previous_state = game.get_state()
            action = learning_agent.get_action(previous_state)

            if (action == BJ.Action.HIT):
                status = game.hit()
                game_history.append([previous_state, action, game.get_state(), step])
                if (status is BJ.Status.GOOD):  # non-terminal state
                    continue
            else:
                status = game.stand()
                game_history.append([previous_state, action, game.get_state(), step])
                if (status is not BJ.Status.STAND):  # non-terminal state
                    continue

            if (game.round == BJ.Round.WIN):
                reward = 1.5
            elif (game.round == BJ.Round.LOSE):
                reward = -1
            elif (game.round == BJ.Round.TIE):
                reward = 0
            else:
                raise ValueError('Error in handling the game status')

            for ele in game_history:
                #reward_recalculated = reward / (step - ele[3] + 1)
                if(step == ele[3]):
                    reward_recalculated = reward
                else:
                    reward_recalculated = 0
                learning_agent.learn(ele[0], ele[1], ele[2], reward_recalculated)
            #if(i > 25000):
           #     learning_agent._epsilon = 0.1

    # print_state_table(learning_agent)
    # print("Imprimer la table")
    # for key, value in sorted(learning_agent._Q.items(), key=lambda x: x[0]):
    #    print("{} : {}".format(key, value))
    print(learning_agent._Q);
    report(play(learning_agent, 1000000))


def report(score):
    print("final result " + str(score))
    tot = sum(score)
    print("Win " + str(score[0] / tot * 100) + "%")
    print("Tie " + str(score[1] / tot * 100) + "%")
    print("Loose " + str(score[2] / tot * 100) + "%")

def print_state_table(learning_table):
    f = open('qtable.csv', 'w', newline='')
    with open('qtable.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["State", "HIT", "STAY"])
        for key, value in sorted(learning_table._Q.items(), key=lambda x: x[0]):
            hit_score = 0
            stand_score = 0

            if (BJ.Action.HIT in value):
                hit_score = value[BJ.Action.HIT]
            if (BJ.Action.STAY in value):
                stand_score = value[BJ.Action.STAY]
            writer.writerow([key, hit_score, stand_score])


def play(learning_table, episodes):
    game = BJ.BlackJack()
    win = 0
    tie = 0
    lose = 0

    for i in range(episodes):
        status = game.deal()
        if (status is BJ.Status.BLACKJACK):
            win += 1
            # print("BlackJack")
            continue
            # Agent turn
        while game.round is None:
            cur_state = game.get_state()
            action = learning_table.get_action(cur_state, False)

            if (action == BJ.Action.HIT):
                game.hit()
            else:
                game.stand()

        if game.round == BJ.Round.WIN:
            win += 1
        elif game.round == BJ.Round.TIE:
            tie += 1
        else:
            lose += 1
    return (win, tie, lose)


test_train_ql()
