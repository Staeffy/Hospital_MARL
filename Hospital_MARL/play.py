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


def play(patient_list, doc_stats, folder_name, rounds=10):

    patients = patient_list
    doc_stats = doc_stats
    treatment_stats = rl_setup.load_json("treatment_stats")

    hosp = rl_setup.Hospital(patients, treatment_stats, doc_stats)

    players=doc_stats.keys()
    initialized_players=[]
    initialized_names=[]

    for player in players:

        player_name=str(player + "_" + doc_stats[player]["strategy"])
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


    file_name=rl_setup.define_file_name(doc_stats,patients,'real')
    #rl_setup.create_folder('stats', folder_name)


    # PLAY WITH LEARNT POLICY
    Rounds = rounds

    for r in range(Rounds):

        print("round", r)

        state1 = ()
        hosp.patient_stats = copy.deepcopy(patients)
        # print("current state is {} with patients to be treated {} ".format(state1, hosp.patient_list))
        # randomly decide which doc starts moving
        n=0
        print("------- TREATMENT ASSIGNMENT --------")  
        while hosp.game_over(state1):
            for player in initialized_players:

                index=initialized_players.index(player)
                name=initialized_names[index]

                doc_orig=list(doc_stats.keys())
                current=doc_orig[index]
                sati_doc=doc_stats[current]['satisfaction']
                satis_pats=rl_setup.get_pat_satisfaction(patients)

                try:
                    unknown_policy=player.unknown_actions
                except:
                    unknown_policy=0

                re, state1, helping,action = player.use_policy(state1)
                #print(f"[{n}.] {name} DOES {action}")
   
                data = [r, name, re, helping, sati_doc, satis_pats, unknown_policy]
                rl_setup.store_data(data,file_name,folder_name)
            n+=1

    print("")
    print("-------- MEDICAL STAFF STATS ------")

    for doc in doc_stats.keys():
        print(f"Satisfaction level of {doc} is {hosp.doc_stats[doc]['satisfaction']}")

    print("")
    print("---------- PATIENT STATS ----------")
    for patient in patients:
        print (f"Satisfaction level of {patient} is {hosp.patient_stats[patient]['satisfaction']}")


    return file_name

#if __name__ == "__main__":

