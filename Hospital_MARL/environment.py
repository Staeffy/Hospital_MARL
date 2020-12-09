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
        """Compare if there are patients in the patient list left that are not 

        Args:
            state ([type]): [description]

        Returns:
            [type]: [description]
        """
        # returns false
        # if any([True for patient in self.patient_list if patient not in state]):
        #     pass
        # else:
        #     pass
        return any(self.patient_list)

    def reset_state(self):
        self.treated_patients=()
        self.patient_list=[]



class Hospital_complex:

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


