import collections
import csv

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

