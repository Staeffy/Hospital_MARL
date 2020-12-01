import random
import numpy as np
import itertools
import matplotlib.pyplot as plt
import pprint
import collections


class Agent:
    def __init__(self, eps=0.1, alpha=0.5):
        self.eps = eps # probability of choosing random action instead of greedy
        self.alpha = alpha # learning rate
        self.verbose = False
        self.state_history = []

    def setV(self, V):
        self.V = V

    def set_symbol(self, sym):
        self.sym = sym

    def set_verbose(self, v):
        # if true, will print values for each position on the board
        self.verbose = v
    
    def random_action(self):
        p = np.random.random()
        available_actions=available_actions_choose_patient(self.state)_history)
        
        if p < (1 - eps):
            print("taking the action as passed in the function",a)
            return a
        else:
            random =np.random.choice(available_actions)
            #print("random generator on, these are the available actions",available_actions)
            print("taking a random choice of available actions",random )
            return random
        

    def reset_history(self):
        self.state_history = []

    def take_action(self, env):
        # choose an action based on epsilon-greedy strategy
     
        if terminal_state(Patients_orig,s):
            #print(terminal_state(Patients_orig,s))

            a = random_action(a,s, self.eps) # epsilon-greedy
            #print("next action is",a)
            r = calculate_patient_reward(a)
            #print("patient List",Patient_list)

            s2 = treat_patient(Patient_list,a,s)
            a2=available_actions_choose_patient(s2)
            print("treated patient/s {} so far. Choosing patient {} to treat next, getting reward {} now the new state is {} and my available actions are {}".format(s,a,r,s2,a2))

            # we will update Q(s,a) AS we experience the episode
            old_qsa = Q[s][a]
            print("old Q(s,a)",old_qsa)
            # the difference between SARSA and Q-Learning is with Q-Learning
            # we will use this max[a']{ Q(s',a')} in our update
            # even if we do not end up taking this action in the next step
            a2, max_q_s2a2 = max_dict(Q[s2])

            print("checking new values for a2,s2",a2, max_q_s2a2 )
            Q[s][a] = Q[s][a] + ALPHA*(r + GAMMA*max_q_s2a2 - Q[s][a])
            biggest_change = max(biggest_change, np.abs(old_qsa - Q[s][a]))

            # we would like to know how often Q(s) has been updated too
            #update_counts[s] = update_counts.get(s,0) + 1

            # next state becomes current state
            s = s2
            a = a2
            print("max dict",a2, max_q_s2a2 )
            print("new a2", a2)
            return s, a 

      # if verbose, draw the board w/ the values
    if self.verbose:
        print("Taking a greedy action")
        for i in range(LENGTH):
        print("------------------")
        for j in range(LENGTH):
            if env.is_empty(i, j):
            # print the value
            print(" %.2f|" % pos2value[(i,j)], end="")
            else:
            print("  ", end="")
            if env.board[i,j] == env.x:
                print("x  |", end="")
            elif env.board[i,j] == env.o:
                print("o  |", end="")
            else:
                print("   |", end="")
        print("")
        print("------------------")

    # make the move
    env.board[next_move[0], next_move[1]] = self.sym

    def update_state_history(self, s):
        # cannot put this in take_action, because take_action only happens
        # once every other iteration for each player
        # state history needs to be updated every iteration
        # s = env.get_state() # don't want to do this twice so pass it in
        self.state_history.append(s)

    def update(self, env):
        # we want to BACKTRACK over the states, so that:
        # V(prev_state) = V(prev_state) + alpha*(V(next_state) - V(prev_state))
        # where V(next_state) = reward if it's the most current state
        #
        # NOTE: we ONLY do this at the end of an episode
        # not so for all the algorithms we will study
        reward = env.reward(self.sym)
        target = reward
        for prev in reversed(self.state_history):
        value = self.V[prev] + self.alpha*(target - self.V[prev])
        self.V[prev] = value
        target = value
        self.reset_history()