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
# own modules

sys.path.append("../")
#sys.path.append("../data")
from agents_simple import Doctor_Q_Learner, Doctor_greedy, Doctor_random
from environment_simple import Hospital
from helpers import store_data, save_policy, show_policies, load_json
from payoff import Payoff_calculator
#from hospData import patients, treatment_stats, doc_stats, load_json


if __name__ == "__main__":


    print("---------------------------------------------------")
    print("            INITIALIZING SIMPLE GAME               ")
    print("---------------------------------------------------")

    patients = ["ANNA", "BELA", "FARIN", "ROD"]
    rewards = [1, 5, 5, 1]
    hosp = Hospital(patients, rewards)

    doc_one = Doctor_Q_Learner(hosp)
    doc_one.initialize_Q()
    doc_two = Doctor_Q_Learner(hosp)
    doc_two.initialize_Q()

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
        current_player_idx = random.choice([0, 1])

        it = 0
        doc_one.biggest_change = 0
        doc_two.biggest_change = 0
        # print(f"--------NEXT ROUND {r} ------ " )

        while hosp.game_over(state):

            if current_player_idx == 0:
                # print("Doc 1 turn")
                current_player = doc_one

            else:
                current_player = doc_two
                # print("Doc 2 turn")

            # print(f"current outside state is {state}")
            # print(f"available patients are: {hosp.patient_stats}")
            state, a, re, ran = current_player.choose_action(state, t)
            # print(f"doing action {a} and getting reward {re}")

            bc = current_player.biggest_change
            it += 1
            data = [r, current_player_idx, it, a, re, bc, ran]
            store_data(data, "training_simple")

            # switch player
            current_player_idx = (current_player_idx + 1) % 2

    stop = time.perf_counter()
    duration=stop-start
    print("")
    print("---------------- FINISHED TRAINING ----------------")
    print("Training took {:.2f} seconds".format(duration))
    # print(f'Q- table for Doc1 is {Doc1.Q}')

    # Retrieve, show and store policies for each doc
    Policy_doc1 = doc_one.get_policy(doc_one.Q)
    Policy_doc2 = doc_two.get_policy(doc_two.Q)

    show_policies(Policy_doc1, "doc1")
    show_policies(Policy_doc2, "doc2")

    save_policy(Policy_doc1, "policy_doc1")
    save_policy(Policy_doc2, "policy_doc2")
