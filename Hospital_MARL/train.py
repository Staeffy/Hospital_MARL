from agent import Doctor
from environment import Hospital_simple as hosp
import os 
import random 
from helpers import store_data, save_policy



if __name__ == "__main__":

    Patients = ["ANNA", "BELA", "FARIN","ROD"]
    rewards = [1, 5, 5, 1]  


    hosp=hosp(Patients, rewards)
    #print("current patients treated", state)
    #print (hosp.treat_patient('ANNA'))
   
    Doc1 = Doctor(hosp)
    Doc1.initialize_Q()

    Doc2=Doctor(hosp)
    Doc2.initialize_Q()
    #print(hosp.treated_patients)
    try:
        os.remove("training.csv") 
        os.remove("real_game.csv") 
    except:
        print("log file does not exist")

    Rounds = 100
    t=1.0
    print('Starting training ')

    for r in range(Rounds):
        if r %100 ==0: 
            t += 1e-2
        if r % 2000 == 0:
            print("it:", r)
       # print("round",t)

        state1=()
        hosp.patient_list=["ANNA", "BELA", "FARIN","ROD"]

        #randomly decide which doc starts moving 
        current_player_idx = random.choice([0,1])
        it=0
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
                

            state1,a,re,ran =current_player.choose_action(state1,t)
            bc=current_player.biggest_change
            it+=1
            data=[r,current_player_idx,it,a,re,bc,ran]
            store_data(data,'training')
            #print(it)
            #next player 
            
            current_player_idx = (current_player_idx + 1)%2
            #print(biggest_change1)
        
        #deltas.append(biggest_change1)

    
    #print(Doc1.Q)
    Policy_doc1=Doc1.get_policy(Doc1.Q)
    Policy_doc2=Doc2.get_policy(Doc2.Q)
    #print(Policy_doc1)

    save_policy(Policy_doc1,'policy_doc1')
  
    save_policy(Policy_doc2, 'policy_doc2')

    # show_policies(Policy_doc1)
    # show_policies(Policy_doc2)

    #PLAY WITH LEARNT POLICY 

    # for r in range(20):
       
    #    # print("round",t)

    #     state1=()
    #     hosp.patient_list=["ANNA", "BELA", "FARIN","ROD"]

    #     #randomly decide which doc starts moving 
    #     current_player_idx = random.choice([0,1])
    
    #     Doc1.biggest_change=0
    #     Doc2.biggest_change=0
    #     while hosp.game_over(state1):
    #         #it=0
    #         if current_player_idx == 0: 
    #             #print("Doc 1 turn")
    #             current_player=Doc1
    #             #it+=1

    #         else:
    #             current_player=Doc2
    #             #print("Doc 2 turn")
                

    #         re,state1=current_player.use_policy(state1)
    #         data=[r,current_player_idx,re]
    #         store_data(data,'real_game')  
    #         current_player_idx = (current_player_idx + 1)%2
  




