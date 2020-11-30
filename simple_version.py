import random
import numpy as np
import itertools
import matplotlib.pyplot as plt
import pprint
import collections

Patients = ["ANNA", "BELA", "FARIN", "ROD"]

rewards = [4, 2, 1, 0]
SMALL_ENOUGH = 1e-3
GAMMA = 0.9
ALPHA = 0.1

def available_actions_choose_patient(cur_state):
    patient_list=Patients_orig
    available_actions = np.setdiff1d(patient_list, cur_state)
    available_actions = list(available_actions)

    if not available_actions:
        print("there are no actions possible")
        return (['nothing'])
        
    else:
        return available_actions
    #print(available_actions)
       

def treat_patient(list_available_patients,patient_to_treat,patients_treated):

    current_state=list(patients_treated)
    #print("currently {} patients have been treated".format(patients_treated))

    if patient_to_treat in list_available_patients:
         #get index of patient to treat
        index = list_available_patients.index(patient_to_treat)
        #print("Patient {} is about to get treated and has index {}".format(patient_to_treat,index))
        #delete patient from available options
        del list_available_patients[index]
        #add treated patient to current state i.e. treated patients 
        # print("new list of available patients is {}".format(list_available_patients))

        current_state.append(patient_to_treat)
        #print("these patients have been treated so far {}".format(current_state))
        return tuple(current_state)


    else: 
        print("patient {} is not in original Patient list, cant be treated".format(patient_to_treat))
        return patients_treated


def calculate_patient_reward(patient):

    if patient in Patients_orig:
        index = Patients_orig.index(patient)
        reward=rewards[index]
        return reward
    else: 
        print("Nice, there are no more patients to treat")
        return 10
    

def determine_winner(player, rewards):
    pass

def terminal_state(Patient_orig_list, patients_treated):
    #print("checking terminal state, patient list {} and treated{}".format(Patient_orig_list, patients_treated))
    
    return any([True for patient in Patient_list if patient not in patients_treated])


def all_possible_states(Patient_list):
    
    a=Patient_list
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


# def combinations(items):
#     return ( set(itertools.compress(items,mask)) for mask in itertools.product(*[[0,1]]*len(items)) )

def random_action(a,state, eps=0.1):
  p = np.random.random()
  available_actions=available_actions_choose_patient(state)
  
  if p < (1 - eps):
    print("taking the action as passed in the function",a)
    return a
  else:
    random =np.random.choice(available_actions)
    #print("random generator on, these are the available actions",available_actions)
    print("taking a random choice of available actions",random )
    return random
    

def show_policies(policy):

    od = collections.OrderedDict(sorted(policy.items()))
    for keys in od:

        
        v=policy[keys]
        if v !='nothing':

            print (" {} treated ----------->  {} next".format(keys,v))
            print("")


def max_dict(d):
  # returns the argmax (key) and max (value) from a dictionary
  # put this into a function since we are using it so often
  max_key = ()
  max_val = float('-inf')
  for k, v in d.items():
    if v > max_val:
      max_val = v
      max_key = k
  return max_key, max_val


if __name__ == '__main__':
   

    #test all_possible_states()
    #print("these are all possible {} states:{}".format(len(test),test))

    Patients_orig = ["ANNA", "BELA","FARI","ROD"]

 
    #initialize all state, action pairs with  Q(s,a) with 0 
    Q = {}
    states = all_possible_states(Patients_orig)
    for s in states:
        state=list(s)
        #print("list state",state)
        Q[s] = {}
        #print("available in Q-table", Q)
        
        possible_actions = available_actions_choose_patient(state) 
        for a in possible_actions:
            #print("for state {} the available actions are {}".format(state,a))
            Q[s][a] = 0
        
    #print (Q)
  
    #keep track of how many times Q[s] has been updated
    update_counts = {}
    update_counts_sa = {}
    for s in states:
        update_counts_sa[s] = {}
        for a in available_actions_choose_patient(state):
            update_counts_sa[s][a] = 1.0
        

    
    # repeat until convergence
    t = 1.0
    deltas = []
    for it in range(5):
        if it % 100 == 0:
            t += 1e-2
        if it % 2000 == 0:
            print("it:", it)

        # instead of 'generating' an epsiode, we will PLAY
        # an episode within this loop
        s = () # start state: no patient treated

        Patient_list = ["ANNA", "BELA","FARI"]

        print("beginning with state{}".format(Q[s]))
        # the first (s, r) tuple is the state we start in and 0
        # (since we don't get a reward) for simply starting the game
        # the last (s, r) tuple is the terminal state and the final reward
        # the value for the terminal state is by definition 0, so we don't
        # care about updating it.
        a, _ = max_dict(Q[s])
        biggest_change = 0
        #print("values for a",)
        print("starting treatment loop")
        print(Q)
        while terminal_state(Patients_orig,s):
            #print(terminal_state(Patients_orig,s))

            a = random_action(a,s, eps=0.5/t) # epsilon-greedy
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
            update_counts[s] = update_counts.get(s,0) + 1

            # next state becomes current state
            s = s2
            a = a2
            print("max dict",a2, max_q_s2a2 )
            print("new a2", a2)
            
            deltas.append(biggest_change)

    plt.plot(deltas)
    plt.show()

    # determine the policy from Q*
    # find V* from Q*
    states=all_possible_states(Patients_orig)
    print(states)
    #state=list(states)
    policy = {}
    V = {}
    for s in states:
        a, max_q = max_dict(Q[s])
        policy[s] = a
        V[s] = max_q

    # what's the proportion of time we spend updating each part of Q?
    print("update counts:")
    total = np.sum(list(update_counts.values()))
    for k, v in update_counts.items():
        update_counts[k] = float(v) / total
        #print(update_counts,k)

    show_policies(policy)
    #print("values:", V)

    #print("policy:",policy)
    # test=pprint.pprint(policy)
    # print(test)
