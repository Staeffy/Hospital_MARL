from agent import Doctor
from environment import Hospital_simple as hosp
import os 
import random 
from helpers import store_data
import numpy as np
from helpers import load_policy 

if __name__ == "__main__":

    Patients = ["ANNA", "BELA", "FARIN","ROD"]
    rewards = [1, 5, 5, 1]  


    hosp=hosp(Patients, rewards)
    #print("current patients treated", state)
    #print (hosp.treat_patient('ANNA'))

    Doc1 = Doctor(hosp)
    Doc2=Doctor(hosp)

    Doc1.policy=load_policy('policy_doc1')
    print(Doc1.policy)

    Doc2.policy=load_policy('policy_doc2')
    print(Doc2.policy)
    # with open("policy_doc1.txt", "r")  as d_doc1:

    #      = d_doc1
    #     print(Doc1.policy)

    # with open("policy_doc2.txt", "r")  as d_doc2:

    #     Doc1.policy = d_doc2
      
   
    
    #PLAY WITH LEARNT POLICY 
    Rounds=20

    for r in range(Rounds):
       
       # print("round",t)

        state1=()
        hosp.patient_list=["ANNA", "BELA", "FARIN","ROD"]

        #randomly decide which doc starts moving 
        current_player_idx = random.choice([0,1])
    
        Doc1.biggest_change=0
        Doc2.biggest_change=0
        while hosp.game_over(state1):
            #it=0
            if current_player_idx == 0: 
                #print("Doc 1 turn")
                current_player=Doc1
                #it+=1

            else:
                current_player=Doc2
                #print("Doc 2 turn")
                

            re,state1=current_player.use_policy(state1)
            data=[r,current_player_idx,re]
            store_data(data,'real_game')  
            current_player_idx = (current_player_idx + 1)%2
  




