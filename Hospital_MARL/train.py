"""Main script to train the doctors. 
    There are two versions - simple and complex. Depending on which should run, game_version needs to be set

"""
#external imports
import os
import random
import copy 
import sys


#own modules
sys.path.append('./rl_setup')
sys.path.append('./data')
from agent import Doctor, Doctor_complex
from environment import Hospital_simple, Hospital_complex
from helpers import store_data, save_policy, show_policies
from payoff import Doc_Payoff
from hospData import Patients, treatment_stats, doc_stats


if __name__ == "__main__":

    game_version='complex'

    if game_version=='simple':
        print('---------------------------------------------------')
        print("            INITIALIZING SIMPLE GAME               ")
        print('---------------------------------------------------')

        Patients = ["ANNA", "BELA", "FARIN","ROD"]
        rewards = [1, 5, 5, 1]
        hosp=Hospital_simple(Patients, rewards)

        Doc1 = Doctor(hosp)
        Doc1.initialize_Q()
        Doc2=Doctor(hosp)
        Doc2.initialize_Q()


    if game_version =='complex':
        print('---------------------------------------------------')
        print("                INITIALIZING COMPLEX GAME          ")
        print('---------------------------------------------------')
        hosp = Hospital_complex(Patients)

        Doc_1_payoff=Doc_Payoff(treatment_stats,doc_stats,'doc1',Patients)
        Doc_2_payoff=Doc_Payoff(treatment_stats,doc_stats,'doc2',Patients)

        Doc1 = Doctor_complex(hosp, doc_stats['doc1']['skills'],Doc_1_payoff, doc_stats)
        Doc2 = Doctor_complex(hosp, doc_stats['doc2']['skills'],Doc_2_payoff, doc_stats)
    

    try:
        #remove old training data 
        os.remove("stats/training.csv")
    except:
        pass

    #set number of rounds to be played
    Rounds = 10000
    # t is used as epsilon-decreasing value 
    t = 1.0
    print("")
    print("-----------------STARTING TRAINING-----------------")

    for r in range(Rounds):
        if r %100 ==0:
            t += 1e-2
        if r % 2000 == 0:
            print("iteration:", r)

        #initial state is empty, and patient list is full 
        state = ()
        hosp.patient_stats = copy.deepcopy(Patients)

        # randomly decide which doc starts moving
        current_player_idx = random.choice([0, 1])

        it = 0
        Doc1.biggest_change = 0
        Doc2.biggest_change = 0
        #print(f"--------NEXT ROUND {r} ------ " )

        while hosp.game_over(state):

            if current_player_idx == 0:
                #print("Doc 1 turn")
                current_player = Doc1

            else:
                current_player = Doc2
                #print("Doc 2 turn")

            #print(f"current outside state is {state}")
            #print(f"available patients are: {hosp.patient_stats}")
            state, a, re, ran = current_player.choose_action(state, t)
            #print(f"doing action {a} and getting reward {re}")

            bc = current_player.biggest_change
            it += 1
            data = [r, current_player_idx, it, a, re, bc, ran]
            store_data(data, 'training')
         
            #switch player 
            current_player_idx = (current_player_idx + 1) % 2
         

    print("")
    print("---------------- FINISHED TRAINING ----------------")

    #print(f'Q- table for Doc1 is {Doc1.Q}')

    #Retrieve, show and store policies for each doc 
    Policy_doc1 = Doc1.get_policy(Doc1.Q)
    Policy_doc2 = Doc2.get_policy(Doc2.Q)

    show_policies(Policy_doc1,'doc1')
    show_policies(Policy_doc2,'doc2')

    save_policy(Policy_doc1, 'policy_doc1')
    save_policy(Policy_doc2, 'policy_doc2')
