from agent import Doctor, Doctor_complex
from environment import Hospital_simple, Hospital_complex
import os 
import random 
from helpers import store_data
import numpy as np
from helpers import load_policy 

if __name__ == "__main__":

    Patients =	{
        "A": ["t1", "t2","t3"],
        "B": ["t3","t4","t1"]
    } 

    rewards={
        't1':5,
        't2':1,
        't3':5,
        't4':1
    }



    hosp=Hospital_complex(Patients, rewards)
    #print("current patients treated", state)
    #print (hosp.treat_patient('ANNA'))

    Doc1 =Doctor_complex(hosp)
    Doc2=Doctor_complex(hosp)

    Doc1.policy=load_policy('policy_doc1')
    print(Doc1.policy)

    Doc2.policy=load_policy('policy_doc2')
    print(Doc2.policy)
    
    try:
        os.remove("real_game.csv") 
    except:
        print("old game file does not exist")
    
    #PLAY WITH LEARNT POLICY 
    Rounds=20

    for r in range(Rounds):
       
       # print("round",t)

        state1=()
        hosp.patient_list=  Patients =	{
        "A": ["t1", "t2","t3"],
        "B": ["t3","t4","t1"]
        } 
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
  




