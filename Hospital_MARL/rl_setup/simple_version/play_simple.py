"""Script to play the allocation game based on the previously trained policies 
"""
# external imports
import os
import random
import copy
import numpy as np
import sys
from numpy.random import permutation

sys.path.append("../")
from agents_simple import Doctor_Q_Learner, Doctor_greedy, Doctor_random
from environment_simple import Hospital
from helpers import store_data, show_policies, load_json, load_policy
from payoff import Payoff_calculator


if __name__ == "__main__":

    patients = ["ANNA", "BELA", "FARIN", "ROD"]
    rewards = [1, 5, 5, 1]
    hosp = Hospital(patients, rewards)

    players = ["Q_learner", "Q_learner"]
    number_of_players = len(players)

    initialized_players = []
    initialized_names = []

    n = 0
    for player in players:

        player_name = "doc_" + str(n) + "_" + player
        initialized_names.append(player_name)
        n += 1

        if player == "Q_learner":
            player_name = Doctor_Q_Learner(hosp)
            initialized_players.append(player_name)
            player_name.policy = load_policy("policy_doc1")

        if player == "greedy":
            player_name = Doctor_greedy(hosp)
            initialized_players.append(player_name)

        if player == "random":
            player_name = Doctor_random(hosp)
            initialized_players.append(player_name)

    print(initialized_names)
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

        while hosp.game_over(state1):
            # randomly decide which doc starts moving
            for player in permutation(initialized_players):

                current_player = player
                index = initialized_players.index(current_player)
                name = initialized_names[index]

                re, state1 = current_player.use_policy(state1)

                data = [r, name, re]
                store_data(data, "real_game")
