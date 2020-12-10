""" The environment for the agents i.e. different versions of a hospital.
    The state is modeled as patients that need to be treated and patients that have been treated already 
    The actions that can be taken are treating patients. 

"""


import copy
import itertools
import numpy as np 

class Hospital_simple():
    """Simplest version of the hospital with a 1 dimensional patient list. 
        One patient only has one treatment to be done, the treatments are assumed to be always successful
        Treatments have no skills assigned to them.  
    """

    def __init__(self, patient_list, reward_list):
        """Initialize the Hospital by providing patients and rewards 

        Args:
            patient_list (list): List of patients to be treated
            reward_list (list): List of rewards that are assigned to patients by the index
        """
        self.patient_list_orig = copy.deepcopy(patient_list) #keep track of original patient list to get the reward
        self.patient_list = patient_list 
        self.treated_patients = ()  #initial state = no patient treated = empty tuple 
        self.reward_per_patient=reward_list 
        #self.winner = None
        self.num_states = len(self.all_possible_states()) # for logs, check total amount of possible states
          
    def available_actions(self,state):
        """provides all possible actions for a given state 

        Args:
            state (tuple): Patients that have been treated already

        Returns:
            list : Available actions for the given state 
        """
        available_actions = np.setdiff1d(self.patient_list, state)
        available_actions = list(available_actions)

        if not available_actions:
            #print("there are no actions possible")
            return (['nothing'])
            
        else:
            return available_actions

    def reward(self, patient):
        """Provides the reward for a given action i.e. Patient treatment

        Args:
            patient (string): Name of the Patient to be treated

        Returns:
            int : Reward for treating the patient 
        """
        # no reward until game is over
        if patient in self.patient_list_orig:
            index  = self.patient_list_orig.index(patient)
            reward = self.reward_per_patient[index]
            return reward
        else: 
            #print("Nice, there are no more patients to treat")
            return 10


    def treat_patient(self,patient,state):
        """Removes a patient from the list of available patients and adds him to the treated patients 

        Args:
            patient (string): Name of the Patient to be treated
            state (tuple): Patients that have been treated already

        Returns:
            [tuple]: [New state after patient was treated]
        """
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
        """For each permutation of the patient list, the possible combiantions are generated  

        Returns:
            set: all possible states of the patient list
        """
            
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
        """Compare if there are patients in the patient list left that are not in the treated patient list yet

        Args:
            state (tuple): Patients that have been treated already

        Returns:
            [boolean]: [Returns false if there are no more patients to be treated]
        """
        # returns false
        # if any([True for patient in self.patient_list if patient not in state]):
        #     pass
        # else:
        #     pass
        return any([True for patient in self.patient_list if patient not in state])

    def reset_state(self):
        
        self.treated_patients=()
        self.patient_list=[]



class Hospital_complex:

    def __init__(self, patient_list, reward_list):
        self.patient_list_orig = copy.deepcopy(patient_list)
        self.patient_list = patient_list
        self.treated_patients = ()
        self.reward_per_patient=reward_list
        #self.winner = None
        #self.num_states = len(self.all_possible_states())
          
    def available_actions(self,state):
        
        available_actions = { k : self.patient_list[k] for k in set(self.patient_list) - set(state) }
        a = []

        #a=dict()
        # for (key,value) in available_actions.items():
        #     a[key] = available_actions[key][0]

        for key in available_actions.keys():
            pat=key
            treat=self.patient_list[key][0]
            action=(pat,treat)
            a.append(action)

        if not available_actions:
            #print("there are no actions possible")
            return (['nothing'])
            
        else:
            return a

    def reward(self, patient):
        # no reward until game is over
        if patient in self.patient_list:
            treatment=self.patient_list[patient][0] 
            reward=self.rewards[str(treatment)]
          
            return reward
        else: 
            #print("Nice, there are no more patients to treat")
            return 0

    def treat_patient(self,patient,state):
        print("currently {} patients have been treated".format(state))
        current_state=list(state)
        patient_n=patient[0] # first index is patient, second is treatment
        t= patient[1] 
        #treatment=patient[1]
        if patient in self.patient_list:
            #get index of patient to treat
            current_treatment=self.patient_list[patient_n][0]

            print("Patient {} is about to get treatment {}".format(patient_n,t))
            #delete patient from available options
            del (self.patient_list[patient_n][0])
            #add treated patient to current state i.e. treated patients 
            print("new list of available patients is {}".format(self.patient_list))

            current_state.append(patient)
            #current_state=tuple(current_state)
            print("these patients have been treated so far {}".format(current_state))    
            return tuple(current_state)
        else: 
            #print("unable to treat {} ",patient)
            return self.treated_patients

    def all_possible_states(self):
            
        patients = self.patient_list.keys()
        #REIHENFOLGE PATIENTEN
        Q = []
        # For every patient 
        for patient in patients: 
            treatments = (self.patient_list[patient])
            patient_treatment = []
            patient_treatment_list = []
            #patient_treatment_list.append((patient,patient_treatment[:]))
            # For every treatment of the patient
            for treatment in treatments:
                patient_treatment.append(treatment)
                patient_treatment_list.append((patient,tuple(patient_treatment[:])))

            Q.append(patient_treatment_list)
        
        #print(len(Q))
        for i in Q:
            a= Q[0]
            b= Q[1]
            c= Q[2]
        
        test=itertools.product(a,b,c)
        new_opt=[]
        for i in test:
            # permutation
            #print('combi ',i)
            permutations = itertools.permutations(i)
            #combination
            #print ('permu',permutations)
            for per in permutations:
                for L in range(0, len(per)+1):
                    for subset in itertools.combinations(per, L):
                        #print('per', per)
                        #print('subset',subset)
                        #print("possible combinations", subset)
                        new_opt.append(subset)

        #short_version=set(new_opt)
        return new_opt



    def game_over(self,state):

        return any({ k : self.patient_list[k] for k in set(self.patient_list) - set(state) })


#if __name__ == "__main__":
    
#     Patient_info =	{
#     "A": ["tx", "ty","tz"],
#     "B": ["ty"],
#     "D": ["ty", "ty","ty"]
# } 

# rewards={
#     'tx':3,
#     'ty':2,
#     'tz':3
# }

# {
#     "A": ["tx", "ty","tz"],
#     "B": ["ty"],
#     "D": ["ty", "ty","ty"]
# } 

# hosp=Hospital_complex(Patient_info, rewards)
# test=hosp.all_possible_states()

# #print(test)

# state = ()
# p1=['A','tx']
# actions=hosp.available_actions(state)
# print(actions)
# treat_pat=hosp.treat_patient(p1,state)
# print(treat_pat)