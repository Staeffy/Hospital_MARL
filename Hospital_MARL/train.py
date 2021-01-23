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
import rl_setup


def train(patient_list, doc_stats, rounds=10):


    print("---------------------------------------------------")
    print("                INITIALIZING COMPLEX GAME          ")
    print("---------------------------------------------------")

    patients = patient_list
    doc_stats = doc_stats
    treatment_stats = rl_setup.load_json("treatment_stats")

    hosp = rl_setup.Hospital(patients, treatment_stats, doc_stats)

    players = doc_stats.keys()
    initialized_players = []
    initialized_names = []

    for player in players:

        player_name = str(player + "_" + doc_stats[player]["strategy"])
        initialized_names.append(player_name)

        if doc_stats[player]["strategy"] == "Q_learner":
            player_name = rl_setup.Doctor_Q_Learner(player, hosp, doc_stats)
            initialized_players.append(player_name)

        if doc_stats[player]["strategy"] == "Random":
            player_name = rl_setup.Doctor_random(player, hosp, doc_stats)
            initialized_players.append(player_name)

    print(initialized_names)
    print(initialized_players)


    folder_name=rl_setup.define_folder_name(doc_stats)
    file_name=rl_setup.define_file_name(doc_stats,patients,'train')

    rl_setup.create_folder('stats', folder_name)


    # set number of rounds to be played
    Rounds = rounds
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
        hosp.patient_stats = copy.deepcopy(patients)
        hosp.doc_stats = copy.deepcopy(doc_stats)

        # randomly decide which doc starts moving

        it = 0
        for player in initialized_players:
            player.biggest_change = 0
            player.reward_sum=0
            #player.unknown_actions=0

        # print(f"--------NEXT ROUND {r} ------ " )

        while hosp.game_over(state):

            for player in permutation(initialized_players):

                current_player = player
                index = initialized_players.index(current_player)
                name = initialized_names[index]

                # print(f"current outside state is {state}")
                # print(f"available patients are: {hosp.patient_stats}")
                if "Q_learner" in name:
                    state, a, re, ran = current_player.choose_action(state, t)
                    bc = current_player.biggest_change
                    unknown_policy= current_player.unknown_actions


                else:
                    re, state, helping,a = current_player.use_policy(state)
                    bc=0
                    ran=1
                    unknown_policy=0
                # print(f"doing action {a} and getting reward {re}")

                doc_orig=list(doc_stats.keys())
                current=doc_orig[index]
                sati_doc=doc_stats[current]['satisfaction']
                satis_pats=rl_setup.get_pat_satisfaction(patients)
                it += 1
                data = [r, name, it, a, current_player.reward_sum, bc, ran, sati_doc, satis_pats,unknown_policy]
                rl_setup.store_data(data, file_name, folder_name)

            # switch player
            # current_player_idx = (current_player_idx + 1) % 2

    stop = time.perf_counter()
    duration = stop - start
    print("")
    print("---------------- FINISHED TRAINING ----------------")
    print("Training took {:.2f} seconds".format(duration))
    # print(f'Q- table for Doc1 is {Doc1.Q}')

    # Retrieve, show and store policies for each doc

    for player in initialized_players:
        index = initialized_players.index(player)
        name = initialized_names[index]

        if "Q_learner" in name:
            policy = player.get_policy(player.Q)
        #rl_setup.show_policies(policy, name)
            rl_setup.save_policy(policy, f"policy_{name}", folder_name)

        print(f"Total payoff of player {name} is {player.reward_sum}")


    return folder_name, file_name, initialized_names
