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
        #print('current patient list', needed_treatments)
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


        filter_available_treatments=[]
        #Only first treatment can be done 
        for patients in todo_treatments.keys():
            if any(todo_treatments[patients]):
                filter_available_treatments.append((patients,todo_treatments[patients][0]))
        
        
        return dict(filter_available_treatments)
          
    def available_actions(self, state, skill):
        

        actions=self.determine_missing_treatments(state)
        #print("patient list {} for state {} ".format(actions,state))
        #print("patient list {} for state {} ".format(actions,state))

            
        #print("patient list {} for state {} ".format(actions,state))

        new=[]
        if any (actions):

            treatments_matching_skill=[(key,value) for key, value in actions.items() if any (item in value for item in skill)]
            treatments_help_needed=[(key,value) for key, value in actions.items() if not any (item in value for item in skill)]

            #print(treatments_matching_skill)
            #print(treatments_help_needed)

            state = transform_tuple_to_dict(state)
            #print(state)
            
            if "Ask for help" in state.keys():
            
                asked_for_help=[value for key, value in state.items() if 'Ask for help' in key]
                #print('Someone is aleady asking for help', asked_for_help)
            else: 
                asked_for_help=[]
                #print('no one is asking for help yet')


            for item in treatments_matching_skill:
                #print("check to help or do standalone", item, asked_for_help)
                can_help=[i for i in asked_for_help if item in i]
                
                if any(asked_for_help):
                    treat_direct=[item for i in asked_for_help if item not in i]
                else: 
                    treat_direct=treatments_matching_skill
                    
                for item in can_help:
                    #print('able help with treatment {}'.format(item))
                    new.append(('help',item[0]))
                    #new.append(('postpone',item))

                #print('treat direct', treat_direct)
                for item in treat_direct:
                    new.append(item)

                
            for item in treatments_help_needed:
                #print('need help with {}'.format(item))
                if any(asked_for_help):
                    need_help=[i for i in asked_for_help if item not in i]
                    for i in need_help:
                    #print('asking for help for {}'.format(item))
                        new.append(('Ask for help',i[0]))  
                else: 
                    new.append(('Ask for help',item)) 


            #print(new)
        return tuple(new)

    def treat_patient(self,action,state):
        #print("currently {} patients have been treated, patient {} will get treated".format(state,action))


        if any(action):
            state = transform_tuple_to_dict(state)
            action_opt=action[0]

            if action_opt==('Ask for help'):
                #print('about to help')
                state[action[0]]=[action[1]]
                patient=0
        
            elif action_opt=='help':
                patient = action[1][0]
                current_treatment= action[1][1]
                del state['Ask for help']        
            else: 
                patient=action[0]
                current_treatment=action[1]

            #add treated patient to current state i.e. treated patients 
            if patient != 0:
                if patient in state:
                    #add treatment to existing patient 
                    #print("adding new patient {} to state{}".format(patient,state, type(state)))
                    state[patient].append(current_treatment)
                else: 
                    #add new patient into list with first treatment
                    #print("adding new patient {}to state{}".format(patient,state, type(state)))
                    state[patient]=[current_treatment]

                #delete patient from available options
                del (self.patient_stats[patient]['treatments'][0])

            formatted_state=transform_dict_to_tuple(state)
            #print('new state', formatted_state)
            return formatted_state
            
        else:
            return state

    def all_possible_states(self,doc_info):
            
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
        #print("all options", all_opt)
        short_version=set(all_opt)

        #print(short_version)
        additional_states=[]
        for a in short_version:
            treatments_for_state=self.available_actions_for_init(a,doc_info)
            additional_states.append(tuple(treatments_for_state))

        short_version=list(short_version)
        combined_states=short_version+additional_states
        #combined_states=tuple(combined_states)
        for i in combined_states:
            print(i)

        return combined_states



    def game_over(self,state):
        """Determines whether a game is over or not by checking if there are treatments left in the check_status dict

        Args:
            state ([tuple]): State consisting of patients that have been treated already including their treatments 
        Returns:
            [Boolean]: Returns True if the game is not over yet 
        """

        check_status=self.determine_missing_treatments(state)
        # status=False
        # if any (check_status):
        #     status=True

        return any (check_status)        


