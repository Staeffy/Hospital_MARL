""" This module contains the agents, i.e. doctors, that interact with the environment,
    i.e. the hospital. For evaluation purposes, three different strategies for the doctors to choose actions
    were implemented. 
    - Doctor_Q_Learner : chooses actions based on Q-function
    - Doctor_greedy: chooses action based on maximum value for the current state
    - Doctor_random: always chooses random actions 

"""
import numpy as np
import random
from typing import Union
from rl_setup import helpers

class Doctor_Q_Learner:
    """Doctors perform actions in their environment, the actions they take depend on their skills
    and they receive a payoff for it.
    """

    def __init__(self, name: str, env: object, doc_stats: dict):
        """Initialize the doctor to be able to perform actions (treat patients / ask for help / help) based on the skills.
        While performing actions, the doctor updates his Q-table and collects the corresponding payoff,
        and can derive a policy based on the Q-table.

        Args:
            name ([type]): Doctor's identity out of all available in doc_stats.
            env ([type]): Should be the hospital which the doctor is interacting with.
            doc_stats ([type]): Information about all doctors.

        """
        self.eps = doc_stats[name]["learning"]["epsilon"]  # Exploitation rate
        self.alpha = doc_stats[name]["learning"]["alpha"]  # Learning-rate
        self.gamma = doc_stats[name]["learning"]["gamma"]  # Discount factor
        self.Q = {}  # Q-table filled during training
        self.policy = {}  # retrieved when training is finished
        self.unknown_actions=0
        self.biggest_change = 0  # corresponds to the change of the Q value which is updated for evaluation

        self.env = env  # the hospital the doctor is working in
        self.skill = doc_stats[name][
            "skills"
        ]  # the skills the doctor has to filter treatments/actions he can perform

        self.reward_sum = 0  # sum of all rewards collected

        self.name = name

    def random_action(self, a: tuple, state: tuple, eps: float) :
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

    def choose_action(
        self, state: tuple, t: float) :
        """Doctor chooses action to take based on Q-learning
            actions possible depend on the state and skill of the doctor

        Args:
            state (tuple): Tuple including patients that have been treated already and whether it was asked for help.
            t (float): Factor to decrease epsilon over time

        Returns:
            s2,a,r,ran: For log purposes: The new state s2, the action a that was chosen,
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
            self.unknown_actions +=1
            self.Q[s] = {}
            possible_actions = self.env.available_actions(state, self.skill)
            if any(possible_actions):
                for a in possible_actions:
                    self.Q[s][a] = 0
            else:
                self.Q[s][()] = 0

        # choose an action based on epsilon-greedy strategy
        a, _ = helpers.max_dict(Q[s])
        a, ran = self.random_action(a, s, self.eps / t)

        # possible actions needed to adjust rewards based on helping others or not
        possible_actions = self.env.available_actions(state, self.skill)
        # get reward for chosen action
        # r = self.payoff_function.get_payoff(a, possible_actions, self.work_time)

        # update Q(s,a) AS the episode is being experienced
        old_qsa = Q[s][a]

        # get new state s2 based on chosen action
        s2, r = self.env.take_action(a, s, self.name)

        # update reward counter
        self.reward_sum += r

        # same as previous, check if next state is tracked already in Q-table, if not -> update
        try:
            Q[s2]
        except KeyError:
            self.Q[s2] = {}
            self.unknown_actions +=1
            possible_actions = self.env.available_actions(s2, self.skill)
            # print("for state {} the actions are {}".format(state,possible_actions))
            if any(possible_actions):
                for action in possible_actions:
                    self.Q[s2][action] = 0
            else:
                self.Q[s2][()] = 0

        # max[a']{ Q(s',a')} needed for Q-function
        a2, max_q_s2a2 = helpers.max_dict(Q[s2])

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

    def get_policy(self, Q: dict) -> dict:
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
            action, max_q_value = helpers.max_dict(Q[s])
            self.policy[s] = action
            V[s] = max_q_value

        return self.policy

    def use_policy(self, state):
        """This function can be used to let the agent act according to the derived policy after training

        Args:
            state (tuple): Current status of treated patients

        Returns:
            int, tuple, int, tuple: reward,  new state, action taken, and whether the agent helped or not
            (1 could help but did not, 0 neutral, -1 could help but did not)
        """
        available_options = self.env.available_actions(state, self.skill)

        try:
            action = self.policy[state]
        except KeyError:
            self.unknown_actions +=1
            action_list = list(available_options)
            rnd_indices = np.random.choice(len(action_list))
            action = action_list[rnd_indices]


        new_state, reward = self.env.take_action(action, state, self.name)
        self.reward_sum += reward
        # print('current state is {} doing action {} new state is {}'.format(state,a,new_state))

        help_behavior_point = self.env.determine_behavior(available_options, action)

        return reward, new_state, help_behavior_point, action


class Doctor_random:
    """Doctor performs random action in the environment, depending on the skills and current state,
    and receives a payoff for the action.
    """

    def __init__(self, name: str, env: object, doc_stats: dict):
        """Initialize the doctor to be able to perform actions (treat patients / ask for help / help) based on the skills.

        Args:
            name ([type]): Doctor's identity out of all available in doc_stats.
            env ([type]): Should be the hospital which the doctor is interacting with.
            doc_stats ([type]): Information about all doctors.

        """

        self.env = env  # the hospital the doctor is working in
        self.skill = doc_stats[name][
            "skills"
        ]  # the skills the doctor has to filter treatments/actions he can perform
        self.name = name
        self.reward_sum = 0  # sum of all rewards collected

    def use_policy(self, state: tuple) :
        """This function chooses and performs the random action based on the current state.

        Args:
            state (tuple): Current state of the environment

        Returns:
            float, tuple, int, tuple: reward, new state, action taken, and whether the agent helped or not
            (1 could help but did not, 0 neutral, -1 could help but did not)
        """
        available_options = self.env.available_actions(state, self.skill)

        if any(available_options):
            action_list = list(available_options)
            rnd_indices = np.random.choice(len(action_list))
            random_action = action_list[rnd_indices]
        else:
            random_action = ()

        new_state, reward = self.env.take_action(random_action, state, self.name)
        self.reward_sum += reward
        
        # print('current state is {} doing action {} new state is {}'.format(state,a,new_state))
        help_behavior_point = self.env.determine_behavior(
            available_options, random_action
        )

        return reward, new_state, help_behavior_point, random_action


class Doctor_greedy:
    """Greedy doctor chooses always the best action within the given state, regardless of the future effect."""

    def __init__(self, name, env, doc_stats):
        """Initialize the doctor to be able to perform actions (treat patients / ask for help / help) based on the skills.

        Args:
            name ([type]): Doctor's identity out of all available in doc_stats.
            env ([type]): Should be the hospital which the doctor is interacting with.
            doc_stats ([type]): Information about all doctors.

        """
        self.env = env  # the hospital the doctor is working in
        self.skill = doc_stats[name][
            "skills"
        ]  # the skills the doctor has to filter treatments/actions he can perform
        self.name = name
        self.reward_sum = 0  # sum of all rewards collected

    def use_policy(self, state: tuple):
        """This function chooses and performs the greedy action based on the current state
        by looping through the rewards that can be gained for all currently available options.

        Args:
            state (tuple): Current state of the environment

        Returns:
            int, tuple, int: reward,  action taken, and whether the agent helped or not
            (1 could help but did not, 0 neutral, -1 could help but did not)
        """
        available_options = self.env.available_actions(state, self.skill)
        best_action = ()
        if any(available_options):
            for action in available_options:
                best_reward = 0
                r = self.env.give_reward(self.name, action, state)
                if r > best_reward:
                    best_reward = r
                    best_action = action
        else:
            pass  # print('current state is {} doing action {} new state is {}'.format(state,a,new_state))

        new_state, reward = self.env.take_action(best_action, state, self.name)
        self.reward_sum += reward

        help_behavior_point = self.env.determine_behavior(
            available_options, best_action
        )

        return reward, new_state, help_behavior_point, best_action
