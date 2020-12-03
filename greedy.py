import random
import numpy as np
import matplotlib.pyplot as plt

#Patient = ["ANNA", "BELA", "FARIN", "ROD"]
rewards = [4, 2, 1, 0]
used_patients = []
Patient_info =	{
    "A": ["tx", "ty","tz"],
    "B": ["ty", "tx", "tz"],
    "C": ["tx", "tx", "ty"],
    "D": ["ty", "ty","ty"]
} 

rewards={
    'tx':3,
    'ty':2,
    'tz':3
}


Patients=list(Patient_info.keys())

def available_actions_choose_patient(agent, not_used_patients):
    rewards_agent = [calculate_reward(patient) for patient in not_used_patients]

    print(not_used_patients)
    print(rewards_agent)
    best_match = np.argmax(rewards_agent)
    #cur_reward= np.max(rewards_agent)
    cur_patient = not_used_patients[best_match]  

    print("{}: Best Match: {} (Reward:{})\n".format(agent, cur_patient, np.max(rewards_agent)))
    return cur_patient


def take_action(patient):
    
    #delete patient that was treated
    current_treatment=Patient_info[patient][0]
    del(Patient_info[patient][0])
    new_state=Patient_info
    
    #print (Patient_info[patient])
    #return remaining list 
    return current_treatment, new_state

def calculate_reward(patient):
        
    treatment=Patient_info[patient][0]
    print(treatment)
    reward=rewards[str(treatment)]
    return reward

def calculate_reward_treatment(treatment):
    return rewards[str(treatment)]

def determine_winner(player, rewards):
    pass

def terminal_state():
    return any([False for patient in Patients if patient not in used_patients])

if __name__ == '__main__':
    count=0
    agent1_patient=0
    agent1_treatments=0
    agent1_rewards=0

    agent2_patient=0
    agent2_treatments=0
    agent2_rewards=0

    test = terminal_state()
    while any([True for patient in Patients if patient not in used_patients]):
        count +=1 
        state = 0
        not_used_patients = np.setdiff1d(Patients, used_patients)

        agent="id1"
        not_used_patients = np.setdiff1d(Patients, used_patients)
        cur_patient = choose_patient(agent, not_used_patients)
        agent1_patient+=1
        
        count+=1

        while any(Patient_info[cur_patient]):
            cur_treatment,state=do_treatment(cur_patient)
            agent1_rewards+=calculate_reward_treatment(cur_treatment)
            agent1_treatments+=1

        used_patients.append(cur_patient)

        agent="id2"
        not_used_patients = np.setdiff1d(Patients, used_patients)
        cur_patient = choose_patient(agent, not_used_patients)
        
        agent2_patient+=1

        while any(Patient_info[cur_patient]):
            cur_treatment,state=do_treatment(cur_patient)
            agent2_rewards+=calculate_reward_treatment(cur_treatment)
            agent2_treatments+=1

        used_patients.append(cur_patient)
        count+=1
        
    print("Done. Selected Patients Order: {}".format(used_patients))
    print ("counts:",count)
    print("Agent 1 stats =", agent1_patient, agent1_treatments, "rewards", agent1_rewards)
    print ("Agent 2 stats", agent2_patient, agent2_treatments, "rewards", agent2_rewards)
 
    # plt.ylabel('Amount patients')
    # plt.xlabel('iterations')

    # plt.plot(agent1_patient, 'r-', label='Patients for agent 1')
    # plt.plot(agent2_patient, 'g-', label='Patients for agend 2')
    # plt.show()   