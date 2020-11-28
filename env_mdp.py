import random
import numpy as np
import matplotlib.pyplot as plt
from helpers import random_action, max_dict

#Patient = ["ANNA", "BELA", "FARIN", "ROD"]
rewards = [4, 2, 1, 0]
used_patients = []
Patient_info =	{
    "A": ["tx", "ty","tz"],
    "B": ["ty", "tx", "tz"],
    "C": ["tx", "tx", "ty"],
    "D": ["ty", "ty","ty"]
} 

rewards={
    'tx':3,
    'ty':2,
    'tz':3
}



SMALL_ENOUGH = 1e-3
GAMMA = 0.9
Patients=list(Patient_info.keys())


def available_actions_choose_patient():
    available_actions = np.setdiff1d(Patients, used_patients)

    #print(available_actions)
    return available_actions

def available_actions_treatments(Patient_info,patient):
    available_actions=Patient_info[patient][0]

    #print("available actions", available_actions)
    return available_actions


def take_action(patient):
    
    #delete patient that was treated
    print("treating patient:", patient)
    current_treatment=Patient_info[patient][0]
    del(Patient_info[patient][0])
    new_state=Patient_info
    
    if any(Patient_info[patient]) ==False:
        used_patients.append(patient)


    reward= calculate_reward_treatment(patient)
    print("reward for patient{} is {}".format(patient,reward) )
    #return remaining list 
    return  new_state, reward

def calculate_reward(patient):
        
    treatment=Patient_info[patient][0]
    print(treatment)
    reward=rewards[str(treatment)]
    return reward

def calculate_reward_treatment(treatment):
    return rewards[str(treatment)]

def determine_winner(player, rewards):
    pass

def terminal_state():
    return any([False for patient in Patients if patient not in used_patients])





if __name__ == '__main__':
   
    #available_actions_choose_patient(Patient_info)


    # initialize Q(s,a)
    Q = {}
    states = available_actions_choose_patient()
    for s in states:
        Q[s] = {}
        #print("available states", Q)
        a = available_actions_treatments(Patient_info,s) 
        Q[s][a] = 0
        
    #print (Q)
  

    t = 1.0
    deltas = []
    for it in range(10000):
        if it % 100 == 0:
            t += 1e-2
        if it % 2000 == 0:
            print("it:", it)

        # play one round 
        # take_random_patient()

        # the first (s, r) tuple is the state we start in and 0
        # (since we don't get a reward) for simply starting the game
        # the last (s, r) tuple is the terminal state and the final reward
        # the value for the terminal state is by definition 0, so we don't
        # care about updating it.
        a, _ = max_dict(Q[s])
        biggest_change = 0
        while not terminal_state():
            a = random_action(a, eps=0.5/t) # epsilon-greedy
            # random action also works, but slower since you can bump into walls
            # a = np.random.choice(ALL_POSSIBLE_ACTIONS)
            s2,r = take_action()
            
            # not_used_patients = np.setdiff1d(Patients, used_patients)

            # a = choose_patient(not_used_patients)
            # agent1_patient+=1
            


            # we will update Q(s,a) AS we experience the episode
            old_qsa = Q[s][a]
            # the difference between SARSA and Q-Learning is with Q-Learning
            # we will use this max[a']{ Q(s',a')} in our update
            # even if we do not end up taking this action in the next step
            a2, max_q_s2a2 = max_dict(Q[s2])
            Q[s][a] = Q[s][a] + ALPHA*(r + GAMMA*max_q_s2a2 - Q[s][a])
            biggest_change = max(biggest_change, np.abs(old_qsa - Q[s][a]))


            # next state becomes current state
            s = s2
            a = a2
            
            deltas.append(biggest_change)

    plt.plot(deltas)
    plt.show()

    # determine the policy from Q*
    # find V* from Q*
    policy = {}
    V = {}
    for s in Patient_info.keys():
        a, max_q = max_dict(Q[s])
        policy[s] = a
        V[s] = max_q





