import numpy as np
import random
import sys 
sys.path.append("../")
from helpers import max_dict

class Doctor_Q_Learner:
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

        # use this max[a']{ Q(s',a')} in the update
        # even if the action is not taken in the next step
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

    
class Doctor_random:
    """[Doctors perform actions in their environment, which is why they need to get the environment as paramenter]"""

    def __init__(self, env, eps=0.01, alpha=0.5):
        """Initialize the doctor to be able to perform actions -> treat patients.
        While performing actions, the doctor updates his self.Q and collects the corresponding payoff and finally reaches the final policy

        Args:
            env (class): Should be the hospital which the doctor is interacting with
            eps (float, optional): Epsilon value which corresponds to the exploration rate. Defaults to 0.01.
            alpha (float, optional): Learning rate alpha which is used for the Q-function. Defaults to 0.5.
        """
 
        self.env = env
        self.payoff = []
        self.biggest_change = (
            0  # this change corresponds to the change of the Q value which is updated
        )
        self.policy = {}


    def use_policy(self, state):
        """This function can be used to let the agent act according to the derived policy after training

        Args:
            state (tuple): Current status of treated patients

        Returns:
            int, tuple: reward and action taken
        """
        available_actions = self.env.available_actions(state)
        random_action = np.random.choice(available_actions)

        new_state = self.env.treat_patient(random_action, state)
        r = self.env.reward(random_action)

        return r, new_state

    
class Doctor_greedy:
    """[Doctors perform actions in their environment, which is why they need to get the environment as paramenter]"""

    def __init__(self, env, eps=0.01, alpha=0.5):

        self.env = env
        self.gamma = 0.9
        self.payoff = []

    def use_policy(self, state):
        """This function can be used to let the agent act according to the derived policy after training

        Args:
            state (tuple): Current status of treated patients

        Returns:
            int, tuple: reward and action taken
        """

        available_actions = self.env.available_actions(state)
        best_action=()
        if any(available_actions):
            for action in available_actions:
                best_reward=0
                r = self.env.reward(action)
                if r > best_reward:
                    best_reward=r
                    best_action=action
        else:
            pass

        new_state = self.env.treat_patient(best_action, state)
        r = self.env.reward(best_action)

        return r, new_state