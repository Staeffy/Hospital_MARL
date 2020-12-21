from agent import Doctor, Doctor_complex
from environment import Hospital_simple, Hospital_complex
from helpers import store_data, save_policy, show_policies
from payoff import Doc_Payoff
from hospData import Patients, treatment_stats, doc_stats
import os
import random
import copy 

if __name__ == "__main__":

    # HOSP SIMPLE VERSION
    # Patients = ["ANNA", "BELA", "FARIN","ROD"]
    # rewards = [1, 5, 5, 1]
    # hosp=Hospital_simple(Patients, rewards)
    # print("----------INITIALIZING SIMPLE DOCTORS-------------")

    # Doc1 = Doctor(hosp)
    # Doc1.initialize_Q()
    # Doc2=Doctor(hosp)
    # Doc2.initialize_Q()

    # COMPLEX VERSION

    hosp = Hospital_complex(Patients, treatment_stats)

    print("----------INITIALIZING COMPLEX DOCTORS-------------")
    
  
    
    Doc_1_payoff=Doc_Payoff(treatment_stats,doc_stats,'doc1',Patients)
    Doc_2_payoff=Doc_Payoff(treatment_stats,doc_stats,'doc2',Patients)

    Doc1 = Doctor_complex(hosp, doc_stats['doc1']['skills'],Doc_1_payoff)
    Doc1.initialize_Q()
    Doc2 = Doctor_complex(hosp, doc_stats['doc2']['skills'],Doc_2_payoff)
    Doc2.initialize_Q()

    try:
        os.remove("training.csv")
    except:
        print("log file does not exist")

    Rounds = 2
    t = 1.0
    print("------------STARTING TRAINING------------------")

    for r in range(Rounds):
        # if r %100 ==0:
        #     t += 1e-2
        # if r % 2000 == 0:
        print("it:", r)

        state = ()
        hosp.patient_stats = copy.deepcopy(Patients)

        # randomly decide which doc starts moving
        current_player_idx = random.choice([0, 1])
        it = 0
        Doc1.biggest_change = 0
        Doc2.biggest_change = 0
        print("------NEW ROUND ------ ", r)
        while hosp.game_over(state):
            # it=0
            if current_player_idx == 0:
                print("Doc 1 turn")
                current_player = Doc1
                # it+=1

            else:
                current_player = Doc2
                print("Doc 2 turn")

            state, a, re, ran = current_player.choose_action(state, t)
            bc = current_player.biggest_change
            it += 1
            data = [r, current_player_idx, it, a, re, bc, ran]
            store_data(data, 'training')
            # print(it)
            # next player

            current_player_idx = (current_player_idx + 1) % 2
         
        #print("---FINAL STATE IS ---- ", state)
        # deltas.append(biggest_change1)

    print(Doc1.Q)
    Policy_doc1 = Doc1.get_policy(Doc1.Q)
    Policy_doc2 = Doc2.get_policy(Doc2.Q)

    # print(Policy_doc1)
    show_policies(Policy_doc1)
    show_policies(Policy_doc2)

    save_policy(Policy_doc1, 'policy_doc1')
    save_policy(Policy_doc2, 'policy_doc2')
