""" This module contains the agents, i.e. doctors, that interact with the environment ,i.e. the hospital. 
    They are modeled as simple Q-Learning agents which first need to learn a policy which they can later on use. 

"""



import numpy as np
import random 
from helpers import max_dict
import collections


class Doctor:
    """[Doctors perform actions in their environment, which is why they need to get the environment as paramenter]
    """

    def __init__(self,env, eps=0.01, alpha=0.5):
        """Initialize the doctor to be able to perform actions -> treat patients.
        While performing actions, the doctor updates his self.Q and collects the corresponding self.payoff and finally reaches the final self.policy

        Args:
            env (class): Should be the hospital which the doctor is interacting with
            eps (float, optional): Epsilon value which corresponds to the exploration rate. Defaults to 0.01.
            alpha (float, optional): Learning rate alpha which is used for the Q-function. Defaults to 0.5.
        """
        self.eps = eps # probability of choosing random action instead of greedy
        self.alpha = alpha 
        self.Q = {}
        #self.state = env.treated_patients
        self.env=env
        self.gamma=0.9
        self.payoff=[]
        self.biggest_change=0  #this change corresponds to the change of the Q value which is updated
        self.policy={}


    def initialize_Q(self):
        """Initialize all  Q(s,a) state, action pairs with 0
        """
    
        states = self.env.all_possible_states()
        #print("these are the possible states", states)
        for s in states:
            #print(s)
            state=list(s)
            self.Q[s] = {}        
            possible_actions = self.env.available_actions(state) 
            for a in possible_actions:
                #print("in this state, the possible actions are",a)
                print("for state {} the available actions are {}".format(state,a))
                self.Q[s][a] = 0

    
    def random_action(self,a,state,eps):
        """performs a random action based on the epsilon-greedy approach

        Args:
            a (string): Action i.e. patient to be treated
            state (tuple): The current state i.e. patients that have been treated already 
            eps (epsilon): [description]

        Returns:
            sting, binary: return the action chosen and whether it was random 1 or not 0 
        """
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
        """Doctor chooses patient to treat based on Q-learning 

        Args:
            state (tuple): Tuple including patients that have been treated already 
            t (float): Factor to decrease epsilon over time

        Returns:
            s2,a,r,ran: For log purposes we return: The new state s2, the patient (action) that was chosen, the reward r received for the patient and whether it was a random action ran or not 
        """
      
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
        """Derives the policy for the doctor based on Q

        Args:
            Q (dict): Collection of state, action pairs with probabilities for reaching the highest expected reward

        Returns:
            dict: The action to choose for every possible state 
        """

        states = Q.keys()
        #print("Available states",states)
        self.policy = {}
        V = {}
        for s in states:
            a, max_q = max_dict(Q[s])
            self.policy[s] = a
            V[s] = max_q
        
        return self.policy




    def use_policy(self,state):
        """This function can be used to let the agent act according to the derived policy after training 

        Args:
            state (tuple): Current status of treated patients 

        Returns:
            int, tuple: reward and action taken 
        """
        
        a = self.policy[state]
        new_state=self.env.treat_patient(a,state)
        r=self.env.reward(a)
        #print('current state is {} doing action {} new state is {}'.format(state,a,new_state))

        return r,new_state