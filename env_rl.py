import itertools
import copy
import numpy as np
from helpers import max_dict, show_policies
import collections 
import random
import matplotlib.pyplot as plt

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
            print("Nice, there are no more patients to treat")
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
            print("unable to treat {} ",patient)
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
        if any([True for patient in self.patient_list if patient not in state]):
            print("")
        else:
            print("game is over")


        return any([True for patient in self.patient_list if patient not in state])
  



class Agent:

    def __init__(self,env, eps=0.1, alpha=0.5):
        self.eps = eps # probability of choosing random action instead of greedy
        self.alpha = alpha # learning rate
        self.Q = {}
        #self.state = env.treated_patients
        self.env=env
        self.gamma=0.9
        self.payoff=0


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

    
    def random_action(self,a,state):
        p = np.random.random()
        available_actions=self.env.available_actions(state)
        
        if p < (1 - self.eps):
            print("taking the action as passed in the function",a)
            return a
        else:
            random =np.random.choice(available_actions)
            #print("random generator on, these are the available actions",available_actions)
            print("taking a random choice of available actions",random )
            return random
        

    def reset_history(self):
        self.state = []

    def choose_action(self,state):
        # choose an action based on epsilon-greedy strategy
     
        #if self.env.ended == False:
            #print(terminal_state(Patients_orig,s))
            Q=self.Q
            s=state
            #print("this is the current state for this agent", s)

            a, _ = max_dict(Q[s])
            #print("for this state, the best action seems to be", a)

            a = self.random_action(a,s) # epsilon-greedy
            #print("next action is",a)
            r = self.env.reward(a)
            self.payoff+=r
            #print("patient List",Patient_list)

            s2 = self.env.treat_patient(a,s)

            a2=self.env.available_actions(s2)
            #print("treated patient/s {} so far. Choosing patient {} to treat next, getting reward {} now the new state is {} and my available actions are {}".format(s,a,r,s2,a2))

            # we will update Q(s,a) AS we experience the episode
            old_qsa = Q[s][a]
            #print("old Q(s,a)",old_qsa)
            # the difference between SARSA and Q-Learning is with Q-Learning
            # we will use this max[a']{ Q(s',a')} in our update
            # even if we do not end up taking this action in the next step
            a2, max_q_s2a2 = max_dict(Q[s2])

            #print("checking new values for a2,s2",a2, max_q_s2a2 )
            Q[s][a] = Q[s][a] + self.alpha*(r + self.gamma * max_q_s2a2 - Q[s][a])
            #biggest_change = max(biggest_change, np.abs(old_qsa - Q[s][a]))

            # we would like to know how often Q(s) has been updated too
            #update_counts[s] = update_counts.get(s,0) + 1

      
            print("new state",s2)
            return s2
            #print("new a2", a2)
           
    def get_policy(self,state):

        states = self.env.all_possible_states()
        policy = {}
        V = {}
        for s in states:
            a, max_q = max_dict(self.Q[s])
            policy[s] = a
            V[s] = max_q

        return policy

    def show_policies(self,policy):

        od = collections.OrderedDict(sorted(policy.items()))
        for keys in od:
            v=policy[keys]
            if v !='nothing':

                print (" {} treated ----------->  {} next".format(keys,v))
                print("")



# def play_game(p1, p2, env):
#     # loops until the game is over
#     current_player = None
#     state=()
#     while env.game_over(state):
        
#         # alternate between players
#         # p1 always starts first
#         if current_player == p1:
            
#             current_player = p2
#             print("P2 turn")
#         else:
#             current_player = p1
#             print("P1 turn")

#         # current player makes a move
#         state,action=current_player.choose_action(state)
    
#     #state=list(state)
#     state=()

#     print("reset state",state)
       

if __name__ == '__main__':
    
    
    Patients = ["ANNA", "BELA", "FARIN"]
    rewards = [4, 2, 1, 0]  



    hosp=Environment(Patients, rewards)
    #print("current patients treated", state)
    #print (hosp.treat_patient('ANNA'))
   
    Doc1=Agent(hosp)
    Doc1.initialize_Q()

    Doc2=Agent(hosp)
    Doc2.initialize_Q()

    T = 20
    for t in range(T):
        print("round",t)

        state1=()
        hosp.patient_list=["ANNA", "BELA", "FARIN"]

        #randomly decide which doc starts moving 
        current_player_idx = random.choice([0,1])
        while hosp.game_over(state1):
            
            if current_player_idx == 0: 
                print("Doc 1 turn")
                current_player=Doc1

            else:
                current_player=Doc2
                print("Doc 2 turn")
       
            state1=current_player.choose_action(state1)
            current_player_idx = (current_player_idx + 1)%2

    # print("Q Table of Doc1",Doc1.Q)
    # print("Q Table of Doc2", Doc2.Q)
    print ("collected payoff Doc 1",Doc1.payoff)
    print ("collected payoff Doc 2",Doc2.payoff)
    
    plt.plot(Doc1.payoff, Doc2.payoff)
    plt.show()

    




