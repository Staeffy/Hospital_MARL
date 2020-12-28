import collections
import csv
import pickle

def show_policies(policy:dict):
  """formatter to print the policies """

  
  print('####################### LEARNT POLICY ###########################')
  print('STATE----------------------------------------------------> ACTION')
  try:
    od = collections.OrderedDict(sorted(policy.items()))

  except: 
    od = policy.keys()
  for keys in od:
      v=policy[keys]
      if v !='nothing':

          print(f" {keys} treated ----------->  {v} next")
          print("")


def max_dict(d:dict):
  """Loop through dict and get max value and key"""

  max_key=max(d, key=d.get)
  max_val=d[max_key]
  
  #print(f"in dict {d} the max value is {max_val} with key {max_key}")
  return max_key, max_val


def store_data(data:list,name:str):
  """Appends rows to file in current folder """

  row=data

  with open('{}.csv'.format(name), 'a') as f: 
      f= csv.writer(f)
      f.writerow(row)



def save_policy(policy:dict, name:str):
  """Stores a pickl file of data in policy folder"""

  with open('policy/'+ name + '.pkl', 'wb') as f:
      pickle.dump(policy, f, pickle.HIGHEST_PROTOCOL)


def load_policy(name:str ) -> object:
  """loads pickl file from policy folder 
  """

  with open('policy/' + name + '.pkl', 'rb') as f:
      return pickle.load(f)

    
def transform_dict_to_tuple(data:dict) -> tuple:

    if type(data)==dict:
        new_format=[]
        for item in data.keys():
            values=data[item]
            values=tuple(values)
            formatting= (item, values)
            new_format.append(formatting)

        return(tuple(new_format))
    else:
        #print(f"Can't transform {data} of type {type(data)} to tuple")
        return data


def transform_tuple_to_dict(data:tuple) -> dict:
    
    new_format={}
    if type(data)==tuple:
        data = dict(data)
        for keys in data.keys():
            dict_values=data[keys]
            dict_values=list(dict_values)
            new_format[keys]=dict_values

        return new_format
    else: 
        return data
