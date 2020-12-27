from helpers import transform_tuple_to_dict
class Doc_Payoff():

    def __init__(self,treatment_stats,doc_info,which_doc,patient_stats):

        self.treatment_stats=treatment_stats #includes treatment / urgency / duration 
        #weights for different factors 
        self.w_u=1      #urgency
        self.w_d=0    #duration
        self.w_k=0    #pat - doc know each other 
        self.w_s=0   #doc = specialist 
        self.w_h=0
        
        
        self.doc_info=doc_info
        self.doc=which_doc
        self.patient_stats=patient_stats #treatments to do , history of doc

    
    def calc_reward(self,action,options):
        #print(action)
        
        if any(action):
            options=transform_tuple_to_dict(options)
            act_opt=action[0]
            help_reward=True

            if ("help" in options.keys()) and (act_opt !='help'):
                #print('doc needs to get punished')
                help_reward=2

            if act_opt=='help':
                patient=action[1][0]
                treatment=action[1][1]
                help_reward=False
                self.doc_info[self.doc]['satisfaction']+=1
            
            elif act_opt =='Ask for help':
                return 0 
            
            else:
                patient = action[0]
                treatment=action[1]

            urgency=self.treatment_stats[treatment]['urgency']
            duration= self.treatment_stats[treatment]['duration']
            #print("doc history for reward",self.patient_stats[patient])

            doc_history=self.patient_stats[patient]['history']
            doc_specialty=self.doc_info[self.doc]['specialty']
            
            if self.doc in doc_history:
                knows_doc=0
                self.patient_stats[patient]['satisfaction']+=1
            else:
                knows_doc=1 
        
            if treatment in doc_specialty:
                specialty=0
                self.doc_info[self.doc]['satisfaction']+=1
            else:
                specialty=1 

            #print( '1 / (', self.w_u , '*' , urgency, '+', self.w_d, '*', duration, '+', self.w_k, '*' , knows_doc, '+', self.w_s, '*',specialty,'+', self.w_h, '*', help_reward, ')')
            reward=1/(self.w_u*urgency+self.w_d*duration+self.w_k*knows_doc+self.w_s*specialty+self.w_h*help_reward)
            #reward=urgency
            print("Reward is {}".format(reward))
            return reward
        else:
            return 0 

    def update_satisfaction(self,action):

        patient = action[0]
        treatment=action[1]



