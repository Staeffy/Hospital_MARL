Patients = {
    "A":    {'treatments': ["t2", "t1"],
                'history': 'doc1',
                'satisfaction':0},
    "B":    {'treatments': ["t2", "t1"],
                'history': [],
                'satisfaction':0},
    }
# Patients = {
#     "A":    {'treatments': ["t1", "t2"],
#                 'history': 'doc1',
#                 'satisfaction':0},
#     "B":    {'treatments': ["t1", "t2", "t3"],
#                 'history': [],
#                 'satisfaction':0},
#     "C":    {'treatments': ["t1"],
#             'history': 'doc2',
#             'satisfaction':0}
# }

treatment_stats ={
    't1':{
        'urgency': 1,
        'duration': 10,
    },
    't2':{
        'urgency': 1,
        'duration': 10
    },
    't3':{
        'urgency': 3,
        'duration': 10
    }
}

doc_stats={
    'doc1':{
        'skills':['t1'],
        'specialty':'t2',
        'satisfaction':0
    },
    'doc2':{
        'skills':['t1','t2'],
        'specialty':'t1',
        'satisfaction':0
    }
}


