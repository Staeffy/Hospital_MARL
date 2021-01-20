"""Script to play the allocation game based on the previously trained policies 
"""
# external imports
import os
import random
import copy
import numpy as np
import sys


sys.path.append("../")
from agents_simple import Doctor_Q_Learner, Doctor_greedy, Doctor_random
from environment_simple import Hospital
from helpers import store_data,  show_policies, load_json, load_policy
from payoff import Payoff_calculator


if __name__ == "__main__":


    patients = ["ANNA", "BELA", "FARIN", "ROD"]
    rewards = [1, 5, 5, 1]
    hosp = Hospital(patients, rewards)

    players=["Q_learner", "greedy"]
    number_of_players=len(players)
    
    initialized_players=[]
    for player in players:
        
        player_name='doc_'+str(players.index(player))+'_'+player
       

        if player=="Q_learner":
            player_name= Doctor_Q_Learner(hosp)
            initialized_players.append(player_name)
            player_name.policy=load_policy('policy_doc1')

        if player =="greedy":
            player_name = Doctor_greedy(hosp)
            initialized_players.append(player_name)

        if player =="random":
            player_name = Doctor_random(hosp)
            initialized_players.append(player_name)

    print(f"these are the initialized players {initialized_players}")

    try:
        os.remove("real_game.csv")
    except:
        print("old game file does not exist")

    # PLAY WITH LEARNT POLICY
    Rounds = 10

    for r in range(Rounds):

        print("round", r)

        state1 = ()
        hosp.patient_list = copy.deepcopy(patients)
        # print("current state is {} with patients to be treated {} ".format(state1, hosp.patient_list))
        # randomly decide which doc starts moving
        current_player_idx = random.choice(range(number_of_players))

        # print(hosp.game_over(state1))
        while hosp.game_over(state1):
            # it=0
            if current_player_idx == 0:
                print("Doc 1 turn")
                current_player = initialized_players[0]
                # it+=1

            else:
                current_player = initialized_players[1]
                print("Doc 2 turn")


            re, state1 = current_player.use_policy(state1)
            # print(state1)
            data = [r, current_player_idx, re]
            store_data(data, "real_game")
            current_player_idx = (current_player_idx + 1) % 2


