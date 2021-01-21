"""Main script to train the doctors. 
    There are two versions - simple and complex. Depending on which should run, game_version needs to be set

"""
# external imports
import os
import random
import copy
import numpy as np
import sys
from numpy.random import permutation
import time

sys.path.append("../")
from agents_simple import Doctor_Q_Learner, Doctor_greedy, Doctor_random
from environment_simple import Hospital
from helpers import store_data, show_policies, load_json, load_policy, save_policy
from payoff import Payoff_calculator


if __name__ == "__main__":

    patients = ["ANNA", "BELA", "FARIN", "ROD"]
    rewards = [1, 5, 5, 1]
    hosp = Hospital(patients, rewards)

    players = ["Q_learner", "Q_learner"]
    number_of_players = len(players)

    initialized_players = []
    initialized_names = []

    n = 0
    for player in players:

        player_name = "doc_" + str(n) + "_" + player
        initialized_names.append(player_name)
        n += 1

        if player == "Q_learner":
            player_name = Doctor_Q_Learner(hosp)
            initialized_players.append(player_name)
            player_name.initialize_Q()
            player_name.policy = load_policy("policy_doc1")

        if player == "greedy":
            player_name = Doctor_greedy(hosp)
            initialized_players.append(player_name)

        if player == "random":
            player_name = Doctor_random(hosp)
            initialized_players.append(player_name)

    try:
        # remove old training data
        os.remove("stats/training.csv")
    except:
        pass

    # set number of rounds to be played
    Rounds = 10000
    # t is used as epsilon-decreasing value
    t = 1.0
    print("")
    print("-----------------STARTING TRAINING-----------------")

    start = time.perf_counter()
    for r in range(Rounds):
        if r % 100 == 0:
            t += 1e-2
        if r % 2000 == 0:
            print("iteration:", r)

        # initial state is empty, and patient list is full
        state = ()
        hosp.patient_list = copy.deepcopy(patients)

        it = 0
        # doc_one.biggest_change = 0
        # doc_two.biggest_change = 0
        # print(f"--------NEXT ROUND {r} ------ " )

        while hosp.game_over(state):

            for player in permutation(initialized_players):

                current_player = player
                index = initialized_players.index(current_player)
                name = initialized_names[index]

                state, a, re, ran = current_player.choose_action(state, t)
                # print(f"doing action {a} and getting reward {re}")

                bc = current_player.biggest_change
                it += 1
                data = [r, name, it, a, re, bc, ran]
                store_data(data, "training_simple")

            # switch player

    stop = time.perf_counter()
    duration = stop - start
    print("")
    print("---------------- FINISHED TRAINING ----------------")
    print("Training took {:.2f} seconds".format(duration))
    # print(f'Q- table for Doc1 is {Doc1.Q}')

    # Retrieve, show and store policies for each doc

    for player in initialized_players:
        policy = player.get_policy(player.Q)
        index = initialized_players.index(player)
        name = initialized_names[index]

        show_policies(policy, name)
        save_policy(policy, name)
