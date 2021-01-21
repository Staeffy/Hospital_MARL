"""Main script to train the doctors. 
    There are two versions - simple and complex. Depending on which should run, game_version needs to be set

"""
# external imports
import os
import random
import copy
import sys
import json
import time 
from numpy.random import permutation
# own modules
sys.path.append("./rl_setup")
sys.path.append("./data")
from agents import Doctor_Q_Learner, Doctor_greedy, Doctor_random
from environment import Hospital
from helpers import store_data, save_policy, show_policies, load_json
from payoff import Payoff_calculator
#from hospData import patients, treatment_stats, doc_stats, load_json


if __name__ == "__main__":



    print("---------------------------------------------------")
    print("                INITIALIZING COMPLEX GAME          ")
    print("---------------------------------------------------")

    patients = load_json('patient_list_single_treatment')
    doc_stats = load_json('doc_stats_train')
    treatment_stats = load_json('treatment_stats')

    hosp = Hospital(patients, treatment_stats, doc_stats)

    players=doc_stats.keys()
    initialized_players=[]
    initialized_names=[]

    for player in players:

        player_name=str(player+'_'+doc_stats[player]['strategy'])
        initialized_names.append(player_name)


        if doc_stats[player]['strategy']=="Q_learner":
            player_name = Doctor_Q_Learner(
            player, hosp, doc_stats
            )
            initialized_players.append(player_name)

    print(initialized_names)
    print(initialized_players)

    try:
        # remove old training data
        os.remove("stats/training.csv")
    except:
        pass

    # set number of rounds to be played
    Rounds = 1000
    # t is used as epsilon-decreasing value
    t = 1.0
    print("")
    print("-----------------STARTING TRAINING-----------------")

    start=time.perf_counter()
    for r in range(Rounds):
        if r % 100 == 0:
            t += 1e-2
        if r % 2000 == 0:
            print("iteration:", r)

        # initial state is empty, and patient list is full
        state = ()
        hosp.patient_stats = copy.deepcopy(patients)

        # randomly decide which doc starts moving

        it = 0
        for player in initialized_players:
            player.biggest_change = 0

        # print(f"--------NEXT ROUND {r} ------ " )

        while hosp.game_over(state):

            for player in permutation(initialized_players):
            
                current_player=player
                index=initialized_players.index(current_player)
                name=initialized_names[index]

                # print(f"current outside state is {state}")
                # print(f"available patients are: {hosp.patient_stats}")
                state, a, re, ran = current_player.choose_action(state, t)
                # print(f"doing action {a} and getting reward {re}")

                bc = current_player.biggest_change
                it += 1
                data = [r, name, it, a, re, bc, ran]
                store_data(data, "training")

            # switch player
            #current_player_idx = (current_player_idx + 1) % 2

    stop = time.perf_counter()
    duration=stop-start
    print("")
    print("---------------- FINISHED TRAINING ----------------")
    print("Training took {:.2f} seconds".format(duration))
    # print(f'Q- table for Doc1 is {Doc1.Q}')

    # Retrieve, show and store policies for each doc

    for player in initialized_players:
        index=initialized_players.index(player)
        name=initialized_names[index]

        policy = player.get_policy(player.Q)
        show_policies(policy, name)
        save_policy(policy, f"policy_{name}")

        print(f"Total payoff of player {name} is {player.reward_sum}")

