import collections
import csv
import pickle

def show_policies(policy):

    od = collections.OrderedDict(sorted(policy.items()))
    for keys in od:

        
        v=policy[keys]
        if v !='nothing':

            print (" {} treated ----------->  {} next".format(keys,v))
            print("")


def max_dict(d):
  # returns the argmax (key) and max (value) from a dictionary
  # put this into a function since we are using it so often
  max_key = ()
  max_val = float('-inf')
  for k, v in d.items():
    if v > max_val:
      max_val = v
      max_key = k
  return max_key, max_val


def store_data(data,name):

    row=data

    with open('{}.csv'.format(name), 'a') as f: 
        f= csv.writer(f)
        f.writerow(row)



def save_policy(policy, name ):
    with open('policy/'+ name + '.pkl', 'wb') as f:
        pickle.dump(policy, f, pickle.HIGHEST_PROTOCOL)

def load_policy(name ):
    with open('policy/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

