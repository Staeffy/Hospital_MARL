import itertools
import numpy as np
from helpers import max_dict, show_policies, store_data
import collections 
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import csv
import os
import complex_reward
import copy 

class Environment:

    def __init__(self, patient_list, reward_list):
        self.patient_list_orig = copy.deepcopy(patient_list)
        self.patient_list = patient_list
        #self.treated_patients = ()
        self.reward_per_patient=reward_list
        #self.winner = None
        self.num_states = len(self.all_possible_states())
          
    def available_actions(self,state):
        
        available_actions = np.setdiff1d(self.patient_list, state)
        available_actions = list(available_actions)

        if not available_actions:
            #print("there are no actions possible")
            return (['nothing'])
            
        else:
            return available_actions

    def reward(self, patient):
        # no reward until game is over
        if patient in self.patient_list_orig:
            index  = self.patient_list_orig.index(patient)
            reward = self.reward_per_patient[index]
            return reward
        else: 
            #print("Nice, there are no more patients to treat")
            return 10

    def treat_patient(self,patient,state):
        #print("currently {} patients have been treated".format(patients_treated))
        current_state=list(state)

        if patient in self.patient_list:
            #get index of patient to treat
            index = self.patient_list.index(patient)
            #print("Patient {} is about to get treated and has index {}".format(patient_to_treat,index))
            #delete patient from available options
            del self.patient_list[index]
            #add treated patient to current state i.e. treated patients 
            # print("new list of available patients is {}".format(list_available_patients))

            current_state.append(patient)
            #current_state=tuple(current_state)
            #print("these patients have been treated so far {}".format(current_state))    
            return tuple(current_state)
        else: 
            #print("unable to treat {} ",patient)
            return self.treated_patients

    def all_possible_states(self):
            
        a=self.patient_list
        all_options=[]
        per = itertools.permutations(a)
        for val in per:
            #print("permutation of", val)
            for L in range(0, len(val)+1):
                for subset in itertools.combinations(val, L):
                    #print("possible combinations", subset)
                    all_options.append(subset)

        short_version= set(all_options)
        return short_version

    def game_over(self,state):
        # returns false
        # if any([True for patient in self.patient_list if patient not in state]):
        #     pass
        # else:
        #     pass
        return any([True for patient in self.patient_list if patient not in state])
  

class Agent:

    def __init__(self,env, eps=0.01, alpha=0.5):
        self.eps = eps # probability of choosing random action instead of greedy
        self.alpha = alpha # learning rate
        self.Q = {}
        #self.state = env.treated_patients
        self.env=env
        self.gamma=0.9
        self.payoff=[]
        self.biggest_change=0
        self.policy={}


    def initialize_Q(self):
        #initialize all state, action pairs with  Q(s,a) with 0 
        
        states = self.env.all_possible_states()
        #print("these are the possible states")
        for s in states:
            #print(s)
            state=list(s)
            self.Q[s] = {}        
            possible_actions = self.env.available_actions(state) 
            for a in possible_actions:
                #print("in this state, the possible actions are",a)
                #print("for state {} the available actions are {}".format(state,a))
                self.Q[s][a] = 0

    
    def random_action(self,a,state,eps):
        p = np.random.random()
        available_actions=self.env.available_actions(state)
        
        if p < (1 - eps):
            #print("taking the action as passed in the function",a)
            return a,0
        else:
            random =np.random.choice(available_actions)
            #print("random generator on, these are the available actions",available_actions)
            #print("taking a random choice of available actions",random )
            return random,1
        

    def reset_history(self):
        self.state = []

    def choose_action(self,state,t):
      
            Q=self.Q
            s=state

            # choose an action based on epsilon-greedy strategy
            a, _ = max_dict(Q[s])
            a,ran = self.random_action(a,s,eps=0.5/t) 

     
            r = self.env.reward(a)
            self.payoff.append(r)
            #print("patient List",Patient_list)

            s2 = self.env.treat_patient(a,s)

            a2=self.env.available_actions(s2)
            #print("treated patient/s {} so far. Choosing patient {} to treat next, getting reward {} now the new state is {} and my available actions are {}".format(s,a,r,s2,a2))

            # update Q(s,a) AS we experience the episode
            old_qsa = Q[s][a]
            #print("old Q(s,a)",old_qsa)
            # the difference between SARSA and Q-Learning is with Q-Learning
            # we will use this max[a']{ Q(s',a')} in our update
            # even if we do not end up taking this action in the next step
            a2, max_q_s2a2 = max_dict(Q[s2])

            #print("checking new values for a2,s2",a2, max_q_s2a2 )
            Q[s][a] = Q[s][a] + self.alpha*(r + self.gamma * max_q_s2a2 - Q[s][a])
            self.biggest_change = max(self.biggest_change, np.abs(old_qsa - Q[s][a]))
            

      
            #print("new state",s2)
            return s2,a,r,ran
           
    def get_policy(self,Q):

        states = Q.keys()
        #print("Available states",states)
        self.policy = {}
        V = {}
        for s in states:
            a, max_q = max_dict(Q[s])
            self.policy[s] = a
            V[s] = max_q
        
        return self.policy

    def show_policies(self,policy):

        od = collections.OrderedDict(sorted(policy.items()))
        for keys in od:
            v=policy[keys]
            if v !='nothing':

                print (" {} treated ----------->  {} next".format(keys,v))
                print("")


    def use_policy(self,state):
        
        a = self.policy[state]
        new_state=self.env.treat_patient(a,state)
        r=self.env.reward(a)
        #print('current state is {} doing action {} new state is {}'.format(state,a,new_state))

        return r,new_state


if __name__ == '__main__':
    
    
    Patients = ["ANNA", "BELA", "FARIN","ROD"]
    rewards = [1, 5, 5, 1]  


    hosp=Environment(Patients, rewards)
    #print("current patients treated", state)
    #print (hosp.treat_patient('ANNA'))
   
    Doc1=Agent(hosp)
    Doc1.initialize_Q()

    Doc2=Agent(hosp)
    Doc2.initialize_Q()
    print(Doc1.Q)
    try:
        os.remove("logs.csv") 
    except:
        print("log file does not exist")

    Rounds = 1
    t=1.0

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

    
    print(Doc1.Q)
    Policy_doc1=Doc1.get_policy(Doc1.Q)
    Policy_doc2=Doc2.get_policy(Doc2.Q)


    # show_policies(Policy_doc1)
    # show_policies(Policy_doc2)

    #PLAY WITH LEARNT POLICY 

    for r in range(20):
       
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
            store_data(data,'real game')  
            current_player_idx = (current_player_idx + 1)%2
  




