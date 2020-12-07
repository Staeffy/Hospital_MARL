import numpy as np
import random 
from helpers import max_dict
import collections


class Doctor:

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
        

    def reset_state(self):
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


    
