"""Calculates the payoff R for a given action by taking patient and doctor information into consideration

    R = 1 / ( urgency + (duration / staff time) + know_each_other + speciality + help_reward )

    Urgency = Level from 1-5, 1 is most urgent 5 is least
    Duration = treatment time in minutes
    know_each_other = 0 or 1, 0 if they know each other
    speciality = if doctor is the specialist / has special interest in the treatment : 0 or 1, 0 if he has
    help_reward = 0 or 1, 1 if doctor had the opportunity to help but did not, 0 if he helped / neutral

    All factors have weights that can be changed within the init def

    Doctor and Patient Satisfaction is updated when:
    1. Patient knows doc
    2. Doc performs treatment that is within his specialty
    3. Doc helps another doc
"""

from helpers import transform_tuple_to_dict


class Payoff_calculator:
    """Calculates the payoff R for a given action by taking patient and doctor information into consideration"""

    def __init__(self, treatment_stats, doc_info, which_doc, patient_stats):
        """Initialize weights for the payoff function as well as storing doc and patient info

        Args:
            treatment_stats (dict): {'treatment':{'urgency':1, 'duration':20 }}
            doc_info (dict): {'doc_name':{'skills':['tx','ty'],'specialty':['tx'], 'satisfaction':1}}
            which_doc (str): 'doc_name'
            patient_stats (dict): {'Patient':{'treatments': ['t1'],'history':['doc1'],'satisfaction':0},
        """

        self.treatment_stats = treatment_stats
        # weights for different factors
        self.w_u = doc_info[which_doc]["preferences"]["w_u"]  # urgency
        self.w_d = doc_info[which_doc]["preferences"]["w_d"]  # duration
        self.w_k = doc_info[which_doc]["preferences"]["w_k"]  # know each other
        self.w_s = doc_info[which_doc]["preferences"]["w_s"]  # doc = specialist
        self.w_h = doc_info[which_doc]["preferences"]["w_h"]  # help reward

        self.doc_info = doc_info
        self.doc = which_doc  # needed to check specialty and update satisfaction
        self.patient_stats = patient_stats  # needed to check if doc / pat know each other and update satisfaction

    def get_payoff(self, action, options, doc_time):
        """Main function that calculates reward

        Args:
            action (tuple): Action that the reward should be based on ('Action', ('Patient', 'Treatment'))
            options (tuple): List of available options the doctor could have performed in the given state

        Returns:
            [float]: Payoff for the given action
        """

        # if there is no action, no reward (0) will be returned
        if any(action):
            options = transform_tuple_to_dict(options)
            act_opt = action[0]
            help_reward = 0

            # check if doc could have helped, but decided not to
            if ("help" in options.keys()) and (act_opt != "help"):
                help_reward = 1

            # update satisfaction level if doc helped
            if act_opt == "help":
                patient = action[1][0]
                treatment = action[1][1]

            elif act_opt == "Ask for help":
                return 0

            # direct treatments
            else:
                patient = action[0]
                treatment = action[1]

            if doc_time == 0:
                doc_time = 0.01
            # get factors for payoff function
            urgency = self.treatment_stats[treatment]["urgency"]
            duration = self.treatment_stats[treatment]["duration"] / doc_time

            doc_history = self.patient_stats[patient]["history"]
            doc_specialty = self.doc_info[self.doc]["specialty"]

            # update patient satisfaction if doc is treating a patient that he has treated before
            if self.doc in doc_history:
                knows_doc = 0
                # self.patient_stats[patient]["satisfaction"] += 1
            else:
                knows_doc = 1

            # update doc satisfaction if he is performing a treatment within his specialty
            if treatment in doc_specialty:
                specialty = 0
                # self.doc_info[self.doc]["satisfaction"] += 1
            else:
                specialty = 1

            ###################
            # Payoff function #
            ##################

            reward = 1 / (
                self.w_u * urgency
                + self.w_d * duration
                + self.w_k * knows_doc
                + self.w_s * specialty
                + self.w_h * help_reward
            )

            # print(f"receiving {reward} as reward")
            return reward
        else:
            return 0
