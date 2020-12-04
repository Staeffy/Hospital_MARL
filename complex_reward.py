import itertools


Patient_info =	{
    "A": ["tx", "ty","tz"],
    "B": ["ty"],
    "C": ["tx", "ty"]
} 

rewards={
    'tx':3,
    'ty':2,
    'tz':3
}

skill_needed={
    'tx':1,
    'ty':2,
    'tz':[1,2]
}


Doc={
    'Doc1':{
        'skill':1},
    'Doc2':{
        'skill':2}
}




all_options=[]




patients = Patient_info.keys()
#REIHENFOLGE PATIENTEN
Q = []
# For every patient 
for patient in patients: 
    treatments = (Patient_info[patient])
    patient_treatment = []
    patient_treatment_list = []
    patient_treatment_list.append((patient,patient_treatment[:]))
    # For every treatment of the patient
    for treatment in treatments:
        patient_treatment.append(treatment)
        patient_treatment_list.append((patient,patient_treatment[:]))

    Q.append(patient_treatment_list)

# print(Q)

permutations = list(itertools.permutations(range(len(patients)),len(patients)))
Q_new = []

seq=('elementsA','elementsB','elementsC')
seq=list(itertools.permutations(seq))
print(seq)

for elementsA in Q[0]:
    for elementsB in Q[1]:
        for elementsC in Q[2]:
            
            Q_new.append([elementsA, elementsB, elementsC])
            Q_new.append([elementsA, elementsC, elementsB])
            Q_new.append([elementsB, elementsA, elementsC])
            Q_new.append([elementsB, elementsC, elementsA])
            Q_new.append([elementsC, elementsB, elementsA])
            Q_new.append([elementsC, elementsA, elementsB])




print(Q_new)
print(len(Q_new))

# def iterate_treatments(index, permutation_length, treatment_list, Q_old):
#     Q_list = []
#     if(index == permutation_length):
#         return treatment_list
#     else:
#         for element in Q_old[index]:
#             treatment_list_new = treatment_list[:]
#             treatment_list_new.append(element)
#             Q_list.extend(iterate_treatments(index+1, permutation_length, treatment_list_new[:], Q_old))
#             print(iterate_treatments(index+1, permutation_length, treatment_list_new[:], Q_old))
#             print('____________________________________')
#     return Q_list

# Q_newnew = iterate_treatments(0,2,[],Q)
# print(Q_newnew)
# print(len(Q_newnew))

# print(Q)
# perQ= itertools.permutations(Q)
# newQ=[]


# for per in perQ:
#     #print(per)
#     print(per)
#     # prodQ=itertools.product(per)
#     # for prod in prodQ:
#     #     newQ.append(prodQ)
    

##Q_new=set(Q_new)
#print(Q_new)

#test = list(itertools.product(*Q))

#print(len(newQ))