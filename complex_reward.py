import itertools


Patient_info =	{
    "A": ["tx", "ty","tz"],
    "B": ["ty"],
    "C": ["tx", "ty"],
    "D": ["ty", "tx"]
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



# per = itertools.permutations(Patient_info)
# for val in per:
#     #print("permutation of", val)
#     for L in range(0, len(val)+1):
#         for subset in itertools.combinations(val, L):
#             #print("possible combinations", subset)
#             all_options.append(subset)

# short_version= set(all_options)

# neue_liste=[]
# per2=itertools.permutations(Patient_info['A'])

# for val in per2:
#     #neue_liste.append(keys)
#     for L in range(0, len(val)+1):
#         for subset in itertools.combinations(val, L):
#             #print("possible combinations", subset)
#             neue_liste.append(subset)
    
# #     all_opt=list(itertools.product(Patient_info[keys], Doc.keys())) 
# #     neue_liste.append(all_opt)
# #     print('keys', keys, 'all opt',all_opt)


keys=Patient_info.keys()
per = itertools.permutations(keys)
#REIHENFOLGE PATIENTEN
Q=[]
for key in keys: 
    #print(key)
    per2=itertools.permutations(Patient_info[key])
    
    for val in per2: 
        #print(val)
        pat=(key,val)
        Q.append(pat)

       
        for L in range(0, len(val)+1):
            for subset in itertools.combinations(val, L):
                #print("sub", subset)
                pat=(key,subset)
                Q.append(pat)
           
#print(Q, len(Q))
short_q=set(Q)
print("short q", short_q, len(short_q))

for l in range(0,len(short_q)+1):
    for subset in itertools.combinations(short_q,L):
        print(subset)
