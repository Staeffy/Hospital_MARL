""" This module contains the agents, i.e. doctors, that interact with the environment,
    i.e. the hospital. They are modeled as simple Q-Learning agents which first need to learn a policy which they can later on use. 
    As described in the readme, the simple version chooses patients without restrictions, the complex doctor chooses patients based on 
    skills he has and further has the ability to ask for help if he is unable to perform an action himself. 
    If one doctor asked for help, another doctor which has the skill can decide whether to help or not. 
"""
import numpy as np
import random
from helpers import max_dict


class Doctor:
    """[Doctors perform actions in their environment, which is why they need to get the environment as paramenter]"""

    def __init__(self, env, eps=0.01, alpha=0.5):
        """Initialize the doctor to be able to perform actions -> treat patients.
        While performing actions, the doctor updates his self.Q and collects the corresponding payoff and finally reaches the final policy

        Args:
            env (class): Should be the hospital which the doctor is interacting with
            eps (float, optional): Epsilon value which corresponds to the exploration rate. Defaults to 0.01.
            alpha (float, optional): Learning rate alpha which is used for the Q-function. Defaults to 0.5.
        """
        self.eps = eps  # probability of choosing random action instead of greedy
        self.alpha = alpha
        self.Q = {}
        # self.state = env.treated_patients
        self.env = env
        self.gamma = 0.9
        self.payoff = []
        self.biggest_change = (
            0  # this change corresponds to the change of the Q value which is updated
        )
        self.policy = {}

    def initialize_Q(self):
        """Initialize all  Q(s,a) state, action pairs with 0"""

        states = self.env.all_possible_states()
        for s in states:
            state = list(s)
            self.Q[s] = {}
            possible_actions = self.env.available_actions(state)
            for a in possible_actions:
                self.Q[s][a] = 0

    def random_action(self, a, state, eps):
        """performs a random action based on the epsilon-greedy approach

        Args:
            a (string): Action i.e. patient to be treated
            state (tuple): The current state i.e. patients that have been treated already
            eps (epsilon): [description]

        Returns:
            sting, binary: return the action chosen and whether it was random 1 or not 0
        """
        p = np.random.random()
        available_actions = self.env.available_actions(state)

        if p < (1 - eps):
            return a, 0
        else:
            random = np.random.choice(available_actions)
            return random, 1

    def reset_state(self):
        self.state = []

    def choose_action(self, state, t):
        """Doctor chooses patient to treat based on Q-learning

        Args:
            state (tuple): Tuple including patients that have been treated already
            t (float): Factor to decrease epsilon over time

        Returns:
            s2,a,r,ran: For log purposes we return: The new state s2, the patient (action) that was chosen,
            the reward r received for the patient and whether it was a random action ran or not
        """

        Q = self.Q
        s = state

        # choose an action based on epsilon-greedy strategy
        a, _ = max_dict(Q[s])

        # print("action determined out of max_dict",a, s)
        a, ran = self.random_action(a, s, eps=0.5 / t)

        r = self.env.reward(a)
        self.payoff.append(r)
        # print("patient List",Patient_list)

        s2 = self.env.treat_patient(a, s)

        a2 = self.env.available_actions(s2)

        # update Q(s,a) AS we experience the episode
        old_qsa = Q[s][a]

        # use this max[a']{ Q(s',a')} in our update
        # even if we do not end up taking this action in the next step
        a2, max_q_s2a2 = max_dict(Q[s2])

        Q[s][a] = Q[s][a] + self.alpha * (r + self.gamma * max_q_s2a2 - Q[s][a])

        self.biggest_change = max(self.biggest_change, np.abs(old_qsa - Q[s][a]))

        return s2, a, r, ran

    def get_policy(self, Q):
        """Derives the policy for the doctor based on Q

        Args:
            Q (dict): Collection of state, action pairs with probabilities for reaching the highest expected reward

        Returns:
            dict: The action to choose for every possible state
        """

        states = Q.keys()
        self.policy = {}
        V = {}
        for s in states:
            a, max_q = max_dict(Q[s])
            self.policy[s] = a
            V[s] = max_q

        return self.policy

    def use_policy(self, state):
        """This function can be used to let the agent act according to the derived policy after training

        Args:
            state (tuple): Current status of treated patients

        Returns:
            int, tuple: reward and action taken
        """

        a = self.policy[state]
        new_state = self.env.treat_patient(a, state)
        r = self.env.reward(a)

        return r, new_state


class Doctor_complex:
    """Doctors perform actions in their environment, the actions they take depend on their skills
    and they receive a payoff for it.
    """

    def __init__(self, env, skill, payoff, eps=0.01, alpha=0.5):
        """Initialize the doctor to be able to perform actions (treat patients / ask for help / help) based on his skills.
        While performing actions, the doctor updates his self.Q and collects the corresponding self.payoff and finally reaches the final self.policy

        Args:
            env (class): Should be the hospital which the doctor is interacting with.
            eps (float, optional): Epsilon value which corresponds to the exploration rate. Defaults to 0.01.
            alpha (float, optional): Learning rate alpha which is used for the Q-function. Defaults to 0.5.
        """
        self.eps = eps  # probability of choosing random action instead of greedy
        self.alpha = alpha  # learning-rate
        self.gamma = 0.9  # discount factor
        self.Q = {}  # Q-table filled during training
        self.policy = {}  # retrieved when training is finished
        self.biggest_change = 0  # corresponds to the change of the Q value which is updated for evaluation

        self.env = env  # the hospital the doctor is working in
        self.skill = skill  # the skills the doctor has to filter treatments/actions he can perform

        self.payoff = payoff  # payoff function to calculate the rewards for his actions
        self.reward_sum = []  # sum of all rewards collected

    def random_action(self, a, state, eps):
        """performs a random action based on the epsilon-decreasing approach

        Args:
            a (tuple): Action i.e. patient and treatment to be done -> (Patient, Treatment) or ('Action', (Patient, Treatment)
            state (tuple): The current state i.e. previous patients, treatments, help-requests
            eps (epsilon): Epsilon value

        Returns:
            list, binary: return the action chosen and whether it was random 1 or not 0
        """
        p = np.random.random()
        available_actions = self.env.available_actions(state, self.skill)

        if p < (1 - eps):
            # in most of the cases it will return the action that was given
            return a, 0
        else:
            # explore through taking random actions
            if any(available_actions):
                action_list = list(available_actions)
                rnd_indices = np.random.choice(len(action_list))
                random_data = action_list[rnd_indices]

                return random_data, 1

            else:
                return (), 1

    def choose_action(self, state, t):
        """Doctor chooses action to take based on Q-learning
            actions possible depend on the state and skill of the doctor

        Args:
            state (tuple): Tuple including patients that have been treated already and whether it was asked for help
            t (float): Factor to decrease epsilon over time

        Returns:
            s2,a,r,ran: For log purposes we return: The new state s2, the action that was chosen,
            the reward r received for the action and whether it was a random action ran or not
        """

        Q = self.Q
        s = state

        # Creating Q-Table through experience.
        # The Q-Table is set up as dictionary of dictionaries consisting of states as keys with respective actions as values.
        # Initially all actions get 0 as value
        # Layout example:
        # Q={
        #   state1:{action1:0
        #          action2:0},
        #   state2:{action3:0,
        #           action1:0}
        # }
        try:
            Q[s]
        except KeyError:
            self.Q[s] = {}
            possible_actions = self.env.available_actions(state, self.skill)
            if any(possible_actions):
                for a in possible_actions:
                    self.Q[s][a] = 0
            else:
                self.Q[s][()] = 0

        # choose an action based on epsilon-greedy strategy
        a, _ = max_dict(Q[s])
        a, ran = self.random_action(a, s, eps=0.5 / t)

        # possible actions needed to adjust rewards based on helping others or not
        possible_actions = self.env.available_actions(state, self.skill)
        # get reward for chosen action
        r = self.payoff.calc_reward(a, possible_actions)
        # update reward counter
        self.reward_sum.append(r)

        # update Q(s,a) AS the episode is being experienced
        old_qsa = Q[s][a]

        # get new state s2 based on chosen action
        s2 = self.env.take_action(a, s)
        # same as previous, check if next state is tracked already in Q-table, if not -> update
        try:
            Q[s2]
        except KeyError:
            self.Q[s2] = {}
            possible_actions = self.env.available_actions(s2, self.skill)
            # print("for state {} the actions are {}".format(state,possible_actions))
            if any(possible_actions):
                for action in possible_actions:
                    self.Q[s2][action] = 0
            else:
                self.Q[s2][()] = 0

        # max[a']{ Q(s',a')} needed for Q-function
        a2, max_q_s2a2 = max_dict(Q[s2])

        #################
        # Q - FUNCTION #
        ################
        #
        # New Q(s,a) = Q(s,a) + alpha [ R(s,a) + gamma(maxQ'(s',a')) - Q(s,a)]
        #
        Q[s][a] = Q[s][a] + self.alpha * (r + self.gamma * max_q_s2a2 - Q[s][a])

        # for logging
        self.biggest_change = max(self.biggest_change, np.abs(old_qsa - Q[s][a]))

        return s2, a, r, ran

    def get_policy(self, Q):
        """Derives the policy for the doctor based on Q

        Args:
            Q (dict): Collection of state, action pairs with probabilities for reaching the highest expected reward

        Returns:
            dict: The action to choose for every possible state
        """

        states = Q.keys()
        self.policy = {}
        V = {}
        for s in states:
            a, max_q = max_dict(Q[s])
            self.policy[s] = a
            V[s] = max_q

        return self.policy

    def use_policy(self, state):
        """This function can be used to let the agent act according to the derived policy after training

        Args:
            state (tuple): Current status of treated patients

        Returns:
            int, tuple, int: reward,  action taken, and whether the agent helped or not
            (1 could help but did not, 0 neutral, -1 could help but did not)
        """
        available_options = self.env.available_actions(state, self.skill)
        available_options = dict(available_options)

        a = self.policy[state]
        new_state = self.env.treat_patient(a, state)
        r = self.payoff.calc_reward(a, state)
        # print('current state is {} doing action {} new state is {}'.format(state,a,new_state))

        helping = 0

        if ("help" in available_options.keys()) and (a[0] != "help"):
            helping = -1

        if ("help" in available_options.keys()) and (a[0] == "help"):
            helping = 1

        return r, new_state, helping
