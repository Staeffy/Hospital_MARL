"""Script to play the allocation game based on the previously trained policies 
"""
# external imports
import os
import random
import copy
import numpy as np
import sys
from numpy.random import permutation


sys.path.append("./rl_setup")
sys.path.append("./data")

# own modules
from agents import  Doctor_Q_Learner, Doctor_random, Doctor_greedy
from environment import Hospital
from helpers import store_data, load_policy, load_json
from payoff import Payoff_calculator


if __name__ == "__main__":

    patients = load_json("patient_list_two_treatments")
    doc_stats = load_json("doc_stats")
    treatment_stats = load_json("treatment_stats")

    hosp = Hospital(patients)

    players=doc_stats.keys()
    initialized_players=[]
    initialized_names=[]

    for player in players:

        player_name=str(player+'_'+doc_stats[player]['strategy'])
        initialized_names.append(player_name)

        player_payoff=Payoff_calculator(treatment_stats, doc_stats, player, patients)

        if doc_stats[player]['strategy']=="Q_learner":
            doctor= Doctor_Q_Learner(
            hosp, doc_stats[player]["skills"], player_payoff, doc_stats
            )
            doctor.policy = load_policy(f"policy_{player_name}")

        if doc_stats[player]['strategy'] =="Greedy":
            doctor = Doctor_greedy(
            hosp, doc_stats[player]["skills"], player_payoff, doc_stats
            )
        if doc_stats[player]['strategy'] =="Random":
            doctor = Doctor_random(
            hosp, doc_stats[player]["skills"], player_payoff, doc_stats
            )

        initialized_players.append(doctor)


    try:
        os.remove("real_game.csv")
    except:
        print("old game file does not exist")

    # PLAY WITH LEARNT POLICY
    Rounds = 10

    for r in range(Rounds):

        print("round", r)

        state1 = ()
        hosp.patient_stats = copy.deepcopy(patients)
        # print("current state is {} with patients to be treated {} ".format(state1, hosp.patient_list))
        # randomly decide which doc starts moving

        while hosp.game_over(state1):
                
            for player in permutation(initialized_players):
            
                index=initialized_players.index(player)
                name=initialized_names[index]

                re, state1, helping = player.use_policy(state1)
                # print(state1)
                data = [r, name, re, helping]
                store_data(data, "real_game")


   

        # print("final state is", state1)
    print("-------- PATIENT STATS ------")
    print(player_payoff.patient_stats)

    print("--------DOC STATS ------")
    print(player_payoff.doc_info)
