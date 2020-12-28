"""Script to play the allocation game based on the previously trained policies 
"""
#external imports 
import os 
import random 
import copy 
import numpy as np
import sys
sys.path.append('./rl_setup')
sys.path.append('./data')

#own modules 
from agent import Doctor, Doctor_complex
from environment import Hospital_simple, Hospital_complex
from helpers import store_data, load_policy
from hospData import Patients, treatment_stats, doc_stats
from payoff import Doc_Payoff


if __name__ == "__main__":

 


    hosp = Hospital_complex(Patients, treatment_stats)
    
    Doc_1_payoff=Doc_Payoff(treatment_stats,doc_stats,'doc1',Patients)
    Doc_2_payoff=Doc_Payoff(treatment_stats,doc_stats,'doc2',Patients)

    Doc1 = Doctor_complex(hosp, doc_stats['doc1']['skills'],Doc_1_payoff, doc_stats)
    Doc2 = Doctor_complex(hosp, doc_stats['doc2']['skills'],Doc_2_payoff, doc_stats)


    Doc1.policy=load_policy('policy_doc1')
    #print(Doc1.policy)

    Doc2.policy=load_policy('policy_doc2')
    print(Doc2.policy)
    
    try:
        os.remove("real_game.csv") 
    except:
        print("old game file does not exist")
    
    #PLAY WITH LEARNT POLICY 
    Rounds=10

    for r in range(Rounds):
       
        print("round",r)

        state1=()
        hosp.patient_stats = copy.deepcopy(Patients)
        #print("current state is {} with patients to be treated {} ".format(state1, hosp.patient_list))
        #randomly decide which doc starts moving 
        current_player_idx = random.choice([0,1])
    
        Doc1.biggest_change=0
        Doc2.biggest_change=0
        #print(hosp.game_over(state1))
        while hosp.game_over(state1):
            #it=0
            if current_player_idx == 0: 
                print("Doc 1 turn")
                current_player=Doc1
                #it+=1

            else:
                current_player=Doc2
                print("Doc 2 turn")
                
            re,state1,helping=current_player.use_policy(state1)
            #print(state1)
            data=[r,current_player_idx,re, helping]
            store_data(data,'real_game')  
            current_player_idx = (current_player_idx + 1)%2

        #print("final state is", state1)
    print("-------- PATIENT STATS ------")
    print(Doc_1_payoff.patient_stats)

    print("--------DOC STATS ------")
    print(Doc_2_payoff.doc_info)



