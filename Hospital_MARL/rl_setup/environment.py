""" The environment for the agents i.e. different versions of a hospital.
    The state is modeled as patients that need to be treated and patients that have been treated already. 
    The actions that can be taken are treating patients.
    - Only one action can be done at a time 

    The complex version restricts the sequence of treatments so that only the first treatments of a patient can be chosen. 
        * determine_missing_treatments : Check which treatments are left to do 
        * available_actions: Check which actions the doctor can take based on his skills (treat patient, ask for help, help )
        * take_action: When doctor chose an action -> update state accordingly
        * game_over: Check if the game is over i.e. no treatments are left
"""

import copy
import itertools
import numpy as np
from helpers import transform_dict_to_tuple, transform_tuple_to_dict

class Hospital:
    """Provides patients that need to be treated and updates the state if a doctor chooses an action"""

    def __init__(self, patient_list):
        """Initial hospital set up

        Args:
            patient_list (dict): Includes information about patients, treatments, their urgency,
                                 skills required, and doctor history
        """
        self.patient_stats = patient_list
        self.treated_patients = ()  # stores the patients that have been treated already

    def determine_missing_treatments(self, finished_treatments):
        """Checks which treatments are still left to do by comparing the state with the patient list

        Args:
            finished_treatments (tuple): Current state including which treatments are finished already

        Returns:
            [dict]: Patients as keys with treatment that can be done as value
        """

        finished_treatments = dict(finished_treatments)
        needed_treatments = self.patient_stats
        todo_treatments = {}

        for patient in needed_treatments.keys():

            if patient in finished_treatments.keys():
                # Some treatments applied already
                patient_todo_treatments = []
                for treatment in needed_treatments[patient]["treatments"]:
                    if treatment not in finished_treatments[patient]:
                        patient_todo_treatments.append(treatment)
                todo_treatments[patient] = patient_todo_treatments
            else:
                # No treatments applied, yet
                todo_treatments[patient] = needed_treatments[patient]["treatments"]

        filter_available_treatments = []
        # Only first treatment can be done
        for patients in todo_treatments.keys():
            if any(todo_treatments[patients]):
                filter_available_treatments.append(
                    (patients, todo_treatments[patients][0])
                )

        # EXAMPLE:
        # available_treatments={'Patient1': 'Treatment',
        #                       'Patient2': 'Treatment'}
        #

        return dict(filter_available_treatments)

    def available_actions(self, state, skill):
        """Based on current state and doctors skills, determines possible actions for the doctor.
            If the doctor has the skill and no one asked for help, he can directly perform the treatment.
            If the doctor does not have the skill for a treatment available, he has to ask for help.
            If someone asked for help for a treatment the doctor has the skill for, he can offer help.

        Args:
            state (tuple): Current state including patients,  treatments, help-requests
            skill (list): The doctors skill matching the treatments to be done

        Returns:
            tuple: ('Action', ('Patient', 'Treatment')) All possible_actions for the doctor given the state and skill
        """

        available_actions = self.determine_missing_treatments(state)

        # filtered actions
        possible_actions = []

        if any(available_actions):

            # out of available actions, find those that match skill
            treatments_matching_skill = [
                (key, value)
                for key, value in available_actions.items()
                if any(item in value for item in skill)
            ]

            # out of available actions, find those that don't match skill
            treatments_help_needed = [
                (key, value)
                for key, value in available_actions.items()
                if not any(item in value for item in skill)
            ]

            # transform state to dictionary for convenience
            state = transform_tuple_to_dict(state)

            # find treatments that someone asked for help for
            if "Ask for help" in state.keys():
                asked_for_help = [
                    value for key, value in state.items() if "Ask for help" in key
                ]
            else:
                asked_for_help = []

            # For treatments matching doctors skill the possible actions are:
            #   1.  Help, if someone requested help
            #   2.  Perform treatment directly, if no one asked for help for it

            for item in treatments_matching_skill:
                # all treatments that someone asked for help for and match doctors skills
                can_help = [i for i in asked_for_help if item in i]

                if any(asked_for_help):
                    # all items that match skill but no one asked for help for
                    treat_direct = [item for i in asked_for_help if item not in i]
                else:
                    # if no one asked for help, all treatments matching skills can be performed directly
                    treat_direct = treatments_matching_skill

                # 1.
                for item in can_help:
                    possible_actions.append(("help", item[0]))

                # 2.
                for item in treat_direct:
                    possible_actions.append(item)

            # Doctors can only request help, if the help for this treatment was not requested already
            for item in treatments_help_needed:

                if any(asked_for_help):
                    need_help = [i for i in asked_for_help if item not in i]
                    for i in need_help:
                        possible_actions.append(("Ask for help", i[0]))
                else:
                    possible_actions.append(("Ask for help", item))

        #
        # EXAMPLE:
        # With specific action:
        # ((        'help', ('A',       't2')),
        # ( 'Ask for help', ('A',       't1')),)
        #       Request^     ^ Patient   ^ Treatment
        #
        # Treat directly:
        # (('A', 't3'),)

        return tuple(possible_actions)

    def take_action(self, action, state):
        """Performs action chosen by the doctor and updates state accordingly.
            If action is 'help': remove old help request and treat patient
            If action is 'Ask for help': return old state including help request
            If action is direct treatment: remove treatment from patient list and add to state

        Args:
            action (tuple):  ('Action', ('Patient', 'Treatment'))
            state (tuple): Current state including patients,  treatments, help-requests

        Returns:
            [tuple]: Updated state
        """
        # if there is no action, nothing changes and old state is returned
        if any(action):

            # transforming state to dict for convenience
            state = transform_tuple_to_dict(state)
            action_opt = action[0]

            if action_opt == ("Ask for help"):
                state[action[0]] = [action[1]]
                patient = 0

            elif action_opt == "help":
                patient = action[1][0]
                current_treatment = action[1][1]
                del state["Ask for help"]
            else:
                patient = action[0]
                current_treatment = action[1]

            # add treated patient to current state i.e. treated patients
            if patient != 0:
                if patient in state:
                    # add treatment to existing patient
                    state[patient].append(current_treatment)
                else:
                    # add new patient into list with first treatment
                    state[patient] = [current_treatment]

                # delete treatment from patient list
                del self.patient_stats[patient]["treatments"][0]
                # only the first index treatment is available, so its enough to know which patient

            # transform state back to tuple so that it can be stored in the Q-table as key
            formatted_state = transform_dict_to_tuple(state)
            return formatted_state

        else:
            return state

    def game_over(self, state):
        """Determines whether a game is over by checking if there are treatments left in the check_status dict

        Args:
            state (tuple): State consisting of patients that have been treated already including their treatments
        Returns:
            [Boolean]: Returns True if the game is not over yet
        """
        check_status = self.determine_missing_treatments(state)

        return any(check_status)
