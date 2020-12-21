import collections
import csv
import pickle

def show_policies(policy):
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
  max_val = 0
  for k, v in d.items():
    if v > max_val:
      max_val = v
      max_key = k
    
    else: 
        max_val =0
        max_key = k
  
  #print("in dict {} the max value is {} with key {}".format(d,max_val, max_key))
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

    




def transform_dict_to_tuple(data):

    if type(data)==dict:
        #print("transforming dict {} into tuple".format(data))
        new_format=[]
        for item in data.keys():
            #new_format.append(item)
            values=data[item]
            values=tuple(values)
            formatting= (item, values)
            new_format.append(formatting)

        return(tuple(new_format))
    else:
        #print("Can't transform {} of type {} to tuple".format(data, type(data)))
        return data


def transform_tuple_to_dict(data):
    
    new_format={}
    if type(data)==tuple:
        #print("transforming tuple {} into dict".format(data))

        data = dict(data)
        for keys in data.keys():
            dict_values=data[keys]
            dict_values=list(dict_values)
            new_format[keys]=dict_values
        #print("new dict is {}".format(new_format))
        return new_format
    else: 
        #print("data of type {} was not transformed into dict".format(type(data)))
        return data
