"""Script to play the allocation game based on the previously trained policies 
"""
# external imports
import os
import random
import copy
import numpy as np
import sys
from numpy.random import permutation

import rl_setup

if __name__ == "__main__":

    patients = rl_setup.load_json("patient_list_single_treatment")
    doc_stats = rl_setup.load_json("doc_stats_play")
    treatment_stats = rl_setup.load_json("treatment_stats")

    hosp = rl_setup.Hospital(patients, treatment_stats, doc_stats)

    players=doc_stats.keys()
    initialized_players=[]
    initialized_names=[]

    for player in players:

        player_name=str(player+'_'+doc_stats[player]['strategy'])
        initialized_names.append(player_name)


        if doc_stats[player]['strategy']=="Q_learner":
            doctor= rl_setup.Doctor_Q_Learner(
            player, hosp, doc_stats
            )
            doctor.policy = rl_setup.load_policy(f"policy_{player_name}")

        if doc_stats[player]['strategy'] =="Greedy":
            doctor = rl_setup.Doctor_greedy(
            player, hosp, doc_stats
            )
        if doc_stats[player]['strategy'] =="Random":
            doctor = rl_setup.Doctor_random(
            player, hosp, doc_stats
            )

        initialized_players.append(doctor)


    try:
        os.remove("real_game.csv")
    except:
        print("old game file does not exist")

    # PLAY WITH LEARNT POLICY
    Rounds = 1

    for r in range(Rounds):

        print("round", r)

        state1 = ()
        hosp.patient_stats = copy.deepcopy(patients)
        # print("current state is {} with patients to be treated {} ".format(state1, hosp.patient_list))
        # randomly decide which doc starts moving

        while hosp.game_over(state1):
            print("------- TREATMENT ASSIGNMENT --------")   
            n=0
            for player in permutation(initialized_players):
                n+=1
                index=initialized_players.index(player)
                name=initialized_names[index]

               
                #print("satisfaction is {}")
                re, state1, helping,action = player.use_policy(state1)
                print(f"[{n}.] {name} DOES {action}")
                # print(state1)
                data = [r, name, re, helping]
                rl_setup.store_data(data, "real_game")


    print("")
    print("-------- MEDICAL STAFF STATS ------")

    for doc in doc_stats.keys():
        print(f"Satisfaction level of {doc} is {hosp.doc_stats[doc]['satisfaction']}")

    print("")
    print("---------- PATIENT STATS ----------")
    for patient in patients:
        print (f"Satisfaction level of {patient} is {hosp.patient_stats[patient]['satisfaction']}")