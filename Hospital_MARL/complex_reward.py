import itertools


Patient_info =	{
    "A": ["tx", "ty","tz"],
    "B": ["ty"],
    "C": ["tx", "ty"],
    #"D": ["tz", "ty"]
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


def get_complex_states():

    Patient_info =	{
    "A": ["tx", "ty","tz"],
    "B": ["ty"],
    "C": ["tx", "ty"],
    #"D": ["tz", "ty"]
    } 


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

    seq=('elementsA','elementsB','elementsC','elementsD')
    seq=list(itertools.permutations(seq))
    print(seq)

    for elementsA in Q[0]:
        for elementsB in Q[1]:
            for elementsC in Q[2]:
                #for elementsD in Q[3]:

                    #for per in permutations:

                        # per['elementsA']=elementsA
                        # per
                        #  Q_new.append([elementsA, elementsB, elementsC])
                
                Q_new.append([elementsA, elementsB, elementsC])
                Q_new.append([elementsA, elementsC, elementsB])
                Q_new.append([elementsB, elementsA, elementsC])
                Q_new.append([elementsB, elementsC, elementsA])
                Q_new.append([elementsC, elementsB, elementsA])
                Q_new.append([elementsC, elementsA, elementsB])


    return Q_new



