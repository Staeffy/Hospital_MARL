import random
import numpy as np

Patient = ["ANNA", "BELA", "FARIN", "ROD"]
rewards = [4, 2, 1, 0]
used_patients = []



def choose_patient(agent, not_used_patients):
    rewards_agent = [calculate_reward(patient, agent) for patient in not_used_patients]

    print(not_used_patients)
    print(rewards_agent)

    best_match = np.argmax(rewards_agent)
    cur_patient = not_used_patients[best_match]
    print("{}: Best Match: {} (Reward:{})\n".format(agent, cur_patient, np.max(rewards_agent)))
    
    return cur_patient

def agent1(state):

    #check current state 
    #choose best option 

    return action 

def calculate_reward(patient, agent):
        
    return random.choice(rewards)

while any([True for patient in Patient if patient not in used_patients]):
    state = 0
    not_used_patients = np.setdiff1d(Patient, used_patients)

    agent="id1"
    not_used_patients = np.setdiff1d(Patient, used_patients)
    cur_patient = choose_patient(agent, not_used_patients)
    used_patients.append(cur_patient)

    agent="id2"
    not_used_patients = np.setdiff1d(Patient, used_patients)
    cur_patient = choose_patient(agent, not_used_patients)
    used_patients.append(cur_patient)

print("Done. Selected Patients Order: {}".format(used_patients))