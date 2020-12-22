class Doc_Payoff():

    def __init__(self,treatment_stats,doc_info,which_doc,patient_stats):

        self.treatment_stats=treatment_stats #includes treatment / urgency / duration 
        #weights for different factors 
        self.w_u=1      #urgency
        self.w_d=0.2    #duration
        self.w_k=0.8    #pat - doc know each other 
        self.w_s=0.5    #doc = specialist 
        
        
        
        self.doc_info=doc_info
        self.doc=which_doc
        self.patient_stats=patient_stats #treatments to do , history of doc

    
    def calc_reward(self,patient_treatment):

        if any(patient_treatment):
            patient = patient_treatment[0]
            #check if patient is in patient list 
            treatment=patient_treatment[1]

            urgency=self.treatment_stats[treatment]['urgency']
            duration= self.treatment_stats[treatment]['duration']
            #print("doc history for reward",self.patient_stats[patient])

            doc_history=self.patient_stats[patient]['history']
            doc_specialty=self.doc_info[self.doc]['specialty']
            
            if self.doc in doc_history:
                knows_doc=True
                self.patient_stats[patient]['satisfaction']+=1
            else:
                knows_doc=False 
        
            if treatment in doc_specialty:
                specialty=True
                self.doc_info[self.doc]['satisfaction']+=1
            else:
                specialty=False 

            print("does Patient {} know Doc {} ? {} ".format(patient, self.doc, knows_doc))

            reward=1/(self.w_u*urgency+self.w_d*duration+self.w_k*knows_doc+self.w_s*specialty)
            #print("Reward is {}".format(reward))
            return reward
            print("patient unknown")
        else: 
            #print("No reward for doing nothing")a
            return 0


    def update_satisfaction(self,patient_treatment):

        patient = patient_treatment[0]
        treatment=patient_treatment[1]



