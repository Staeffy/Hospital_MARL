from env import Patient_info, rewards, terminal_state
import pandas as pd
import itertools

from itertools import combinations,chain
from itertools import compress, product



a =	{
    "A": ["tx", "ty","tz"],
    "B": ["ty", "tx", "tz"],
    "C": ["tx", "tx", "ty"],
    "D": ["ty", "ty","ty"]
} 

treatment_list = pd.DataFrame(a)



def combinations(a):
    return ( set(compress(a,mask)) for mask in product(*[[0,1]]*len(a)) )


# for L in range(0, len(a)+1):
#     for subset in itertools.combinations(a, L):
#         print(subset)


# all_combinations = []
# list1_permutations = itertools.permutations(Pat, len(Doc))
# for each_permutation in list1_permutations:

#     zipped = zip(each_permutation, Doc)

#     all_combinations.append(list(zipped))

# print(all_combinations)
# print(len(all_combinations))


def get_state(treatment_list):
    # returns the current state, represented as an int
    # from 0...|S|-1, where S = set of all possible states
    # |S| = 3^(treatment_list SIZE), since each cell can have 3 possible values - empty, x, o
    # some states are not possible, e.g. all cells are x, but we ignore that detail
    # this is like finding the integer represented by a base-3 number
    k = 0
    h = 0
    for i in range(4):
      for j in range(3):

        if treatment_list[i,j] == x:
          v = 1
        if treatment_list[i,j] == o:
          v = 2
        else:
            v=0
        h += (3**k) * v
        k += 1
    return h



def patient_reward_matrix(all_states):
    new=all_states
    for rewards in r: 
        if rewards in new.values:
            new=new.replace([rewards],r[rewards])
            #print(new)
    return new


if __name__ == '__main__':

    print(all_states)

