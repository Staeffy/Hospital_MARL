"""Script to play the allocation game based on the previously trained policies 
"""
# external imports
import os
import random
import copy
import numpy as np
import sys

sys.path.append("./rl_setup")
sys.path.append("./data")

# own modules
from agents import Doctor, Doctor_complex, Doctor_random, Doctor_greedy
from environment import Hospital_simple, Hospital_complex
from helpers import store_data, load_policy, load_json
from payoff import Payoff_calculator


if __name__ == "__main__":

    patients = load_json("patient_list_two_treatments")
    doc_stats = load_json("doc_stats")
    treatment_stats = load_json("treatment_stats")

    hosp = Hospital_complex(patients)

    player_one = "random"
    player_two = "Q_learner"

    if player_one == "Q_learner":
        doc_one_payoff = Payoff_calculator(treatment_stats, doc_stats, "doc1", patients)
        doc_one = Doctor_complex(
            hosp, doc_stats["doc1"]["skills"], doc_one_payoff, doc_stats
        )

    if player_one == "random":
        doc_one_payoff = Payoff_calculator(treatment_stats, doc_stats, "doc1", patients)
        doc_one = Doctor_random(
            hosp, doc_stats["doc1"]["skills"], doc_one_payoff, doc_stats
        )
        doc_one.policy = load_policy("policy_doc1")
    

    if player_one == "greedy":
        doc_one_payoff = Payoff_calculator(treatment_stats, doc_stats, "doc1", patients)
        doc_one = Doctor_greedy(
            hosp, doc_stats["doc1"]["skills"], doc_one_payoff, doc_stats
        )
        doc_one.policy = load_policy("policy_doc1")

    if player_two == "Q_learner":
        doc_two_payoff = Payoff_calculator(treatment_stats, doc_stats, "doc2", patients)
        doc_two = Doctor_complex(
            hosp, doc_stats["doc2"]["skills"], doc_two_payoff, doc_stats
        )
        doc_two.policy = load_policy("policy_doc2")

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
        current_player_idx = random.choice([0, 1])

        doc_one.biggest_change = 0
        doc_two.biggest_change = 0
        # print(hosp.game_over(state1))
        while hosp.game_over(state1):
            # it=0
            if current_player_idx == 0:
                print("Doc 1 turn")
                current_player = doc_one
                # it+=1

            else:
                current_player = doc_two
                print("Doc 2 turn")

            re, state1, helping = current_player.use_policy(state1)
            # print(state1)
            data = [r, current_player_idx, re, helping]
            store_data(data, "real_game")
            current_player_idx = (current_player_idx + 1) % 2

        # print("final state is", state1)
    print("-------- PATIENT STATS ------")
    print(doc_one_payoff.patient_stats)

    print("--------DOC STATS ------")
    print(doc_two_payoff.doc_info)
