import collections
import csv
import pickle

def show_policies(self,policy):
  """formatter for the policies 

    Args:
        policy (dict): The action to choose for every possible state
  """

  od = collections.OrderedDict(sorted(policy.items()))
  for keys in od:
      v=policy[keys]
      if v !='nothing':

          print (" {} treated ----------->  {} next".format(keys,v))
          print("")


def max_dict(d):
  """Loop through dict and get max value and key

  Args:
      d ([dict]): [Dictionary to find the max value for ]

  Returns:
      [tuple]: [Returns the argmax (key) and max (value) from the dict]
  """
  max_key = ()
  max_val = float('-inf')
  for k, v in d.items():
    if v > max_val:
      max_val = v
      max_key = k
  return max_key, max_val


def store_data(data,name):
  """Appends rows in a file 

  Args:
      data (list): [The data to be written in rows]
      name (string): [The name of the file]
  """

  row=data

  with open('{}.csv'.format(name), 'a') as f: 
      f= csv.writer(f)
      f.writerow(row)



def save_policy(data, name ):
  """Writes a pickl dump file of data

  Args:
      policy (dict): data that should be dumped
      name (string): name of the file
  """

  with open('policy/'+ name + '.pkl', 'wb') as f:
      pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def load_policy(name ):
  """loads pickl file 

  Args:
      name (string): name of the file 

  Returns:
      [object]: [the file to be loaded]
  """
  with open('policy/' + name + '.pkl', 'rb') as f:
      return pickle.load(f)

