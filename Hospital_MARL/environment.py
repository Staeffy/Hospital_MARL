""" The environment for the agents i.e. different versions of a hospital.
    The state is modeled as patients that need to be treated and patients that have been treated already 
    The actions that can be taken are treating patients. 

"""


import copy
import itertools
import numpy as np 
from helpers import transform_dict_to_tuple, transform_tuple_to_dict

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
        self.patient_stats = patient_list
        self.treated_patients = ()
        self.reward_per_patient=reward_list
        #self.winner = None
        #self.num_states = len(self.all_possible_states())


    # determine missing treatments 
    def determine_missing_treatments(self,finished_treatments):
        #convert to dict 
        #print("finished treatments to determine missing treatments:", finished_treatments)
        #print("type of state", finished_treatments)
        finished_treatments= dict(finished_treatments)
        needed_treatments = self.patient_stats

        todo_treatments = {}

        for patient in needed_treatments.keys():
            #print(patient)
            if patient in finished_treatments.keys():
                # Some treatments applied already
                patient_todo_treatments = []
                for treatment in needed_treatments[patient]['treatments']:
                    if not treatment in finished_treatments[patient]:
                        patient_todo_treatments.append(treatment)
                todo_treatments[patient] = patient_todo_treatments
            else:
                #No treatments applied, yet
                todo_treatments[patient] = needed_treatments[patient]['treatments']

        return todo_treatments
          
    def available_actions(self, state, skill):
        
        actions=self.determine_missing_treatments(state)
        print(actions)
        new={}
        for keys in actions.keys():
            if any (actions[keys]):
                
                #check if doctor has the skill to perform the action 
                if actions[keys][0] in skill:
                    new[keys]=actions[keys][0]

        #print("for state {} the available actions are {}".format(state,new))
        return new

    def reward(self, patient_treatment):
        # no reward until game is over
        #in tuple patient, the first index is the patient and the second the treatment 
        #print("getting reward for patient", patient_treatment)
        if any(patient_treatment):
            patient = patient_treatment[0]
            if patient in self.patient_stats:
                treatment=patient_treatment[1]

                urgency=self.reward_per_patient[treatment]['urgency']
                duration= self.reward_per_patient[treatment]['duration']

                reward=1/(urgency+duration)
                #print("Reward is {}".format(reward))
                return reward
            else:
                print("patient unknown")
                return 0
        else: 
            #print("No reward for doing nothing")
            return 0

    def treat_patient(self,patient_treatment,state):
        #print("currently {} patients have been treated, patient {} will get treated".format(state,patient))
        
        #if self.game_over(state):
       
        if any(patient_treatment):
            #print("about to treat patient",patient_treatment)
            patient=patient_treatment[0]
            current_treatment=patient_treatment[1]
            state=transform_tuple_to_dict(state)
            #print("current patient list", self.patient_list)
        
            #print("next patient is {} with treatment {}".format(patient,current_treatment))
            #add treated patient to current state i.e. treated patients 
            if patient in state:
                #add treatment to existing patient 
                #print("Patient {} was treated before".format(patient))
                state[patient].append(current_treatment)
                #print("new state is {}".format(state))
            else: 
                #add new patient into list with first treatment
                #print("Patient {} is new ".format(patient))
                state[patient]=[current_treatment]
                #print("new state is {}".format(state))
            #current_state=tuple(state)

            #print("Patient {} is about to get treatment {}".format(patient,current_treatment))
            #delete patient from available options
            del (self.patient_stats[patient]['treatments'][0])
            #print("new list of available patients is {}".format(self.patient_list))

            formatted_patient_list=transform_dict_to_tuple(state)

            return formatted_patient_list
        else:
            #print("patient {} cant be treated".format(patient))
            return state
        
        # else:
        #     print("no patients left to be treated", state)
        #     return state
      



    def all_possible_states(self):
            
        patients = self.patient_stats.keys()
        #REIHENFOLGE PATIENTEN
        Q = []
        # For every patient 
        for patient in patients: 
            treatments = (self.patient_stats[patient]['treatments'])
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
            #c= Q[2]
        
        test=itertools.product(a,b)
        #test=itertools.product(a,b,c)

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

        #work around to remove duplicate entries
        all_opt=list(new_opt)
        short_version=set(all_opt)
        return short_version



    def game_over(self,state):

        check_status=self.determine_missing_treatments(state)
        for keys in check_status.keys():
            if any (check_status[keys]):

                #print("there is something to do")
                return True
            else:
                #print("game is over")
                return False

        #return any({ k : self.patient_list[k] for k in set(self.patient_list) - set(state) })


